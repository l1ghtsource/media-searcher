import os
from time import time
import requests
import faiss
import numpy as np
import clickhouse_connect
import torch
import pandas as pd
from fastapi import FastAPI
from sklearn.metrics.pairwise import cosine_similarity
from transformers import CLIPTokenizer, CLIPTextModelWithProjection
from sentence_transformers import util
from fast_autocomplete import AutoComplete
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sklearn.cluster import AgglomerativeClustering
from models import Base, Face, Video, Cluster


CLICKHOUSE_HOST = os.environ['CLICKHOUSE_HOST']
CLICKHOUSE_USERNAME = os.environ['CLICKHOUSE_USERNAME']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']

TRANSLATOR_URL = os.environ['TRANSLATOR_URL']
TEXTEMBEDDER_URL = os.environ['TEXTEMBEDDER_URL']

KAFKA_URL = os.environ['KAFKA_URL']

POSTGRES_URL = os.environ['POSTGRES_URL']

engine = create_engine(POSTGRES_URL, pool_pre_ping=True)


def build_embeddings(text):
    return requests.get(TEXTEMBEDDER_URL + '/build_embeddings', json={'text': text}).json()['embeddings']


def translate_text(text):
    return requests.get(TRANSLATOR_URL + '/translate', json={'text': text}).json()['translation']


def download_models():
    if len(os.listdir("/clip_model")) == 0:
        print('download')
        model = CLIPTextModelWithProjection.from_pretrained("Searchium-ai/clip4clip-webvid150k")
        model.save_pretrained("/clip_model")
        tokenizer = CLIPTokenizer.from_pretrained("Searchium-ai/clip4clip-webvid150k")
        tokenizer.save_pretrained("/clip_model")


download_models()


class Text2CLIPModel:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPTextModelWithProjection.from_pretrained("/clip_model").to(self.device)
        self.tokenizer = CLIPTokenizer.from_pretrained("/clip_model")

    def get_text_embedding(self, text):
        inputs = self.tokenizer(text=text, return_tensors="pt").to(self.device)
        outputs = self.model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
        final_output = outputs[0] / outputs[0].norm(dim=-1, keepdim=True)
        final_output = final_output.cpu().detach().numpy()

        return final_output


class SimilarityRanker:
    def __init__(self):
        self.cliptext = Text2CLIPModel()
        self.known_updated = 0
        self.load_from_db()

    def load_from_db(self):
        ctime = time()
        if ctime - self.known_updated > 7200:
            with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
                self.db = client.query_df(
                    f'SELECT id, clip_emb, ocr_emb, whisper_emb, whisper_len, ocr_len FROM embeddings')
            self.index_clip = self.create_faiss_index(np.vstack(self.db['clip_emb'].values).astype('float32'))
            self.index_ocr = self.create_faiss_index(np.vstack(self.db['ocr_emb'].values).astype('float32'))
            self.index_whisper = self.create_faiss_index(np.vstack(self.db['whisper_emb'].values).astype('float32'))
            self.known_updated = ctime

    def create_faiss_index(self, embeddings):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index

    def get_weights(self, word_whisper_count, word_ocr_count):
        max_count = 77

        w_1 = (word_ocr_count / (max_count + word_ocr_count))
        w_2 = (word_whisper_count / (max_count + word_whisper_count))

        ocr_weight = 0.05 * w_1
        whisper_weight = 0.05 * w_2
        clip_weight = 0.9 * (1 - (w_1 + w_2) / 2)

        ocr_weight, whisper_weight, clip_weight = np.exp(
            [ocr_weight, whisper_weight, clip_weight]) / np.sum(np.exp([ocr_weight, whisper_weight, clip_weight]))

        return clip_weight, ocr_weight, whisper_weight

    def find_top_k(self, text, k=5):
        text = translate_text(text)

        text_emb = np.array(build_embeddings(text), dtype='float32')
        clip_emb = self.cliptext.get_text_embedding(text).astype('float32')
        text_emb = text_emb.astype('float32')

        _, clip_indices = self.index_clip.search(clip_emb.reshape(1, -1), k)
        _, ocr_indices = self.index_ocr.search(text_emb.reshape(1, -1), k)
        _, whisper_indices = self.index_whisper.search(text_emb.reshape(1, -1), k)

        unique_indices = set(clip_indices[0]).union(ocr_indices[0]).union(whisper_indices[0])

        best_videos = []
        for i in unique_indices:
            id_, video_clip_emb, video_ocr_emb, video_whisper_emb, word_whisper_count, word_ocr_count = self.db.iloc[i]

            video_clip_emb = np.array(video_clip_emb).astype('float32')
            video_ocr_emb = np.array(video_ocr_emb).astype('float32')
            video_whisper_emb = np.array(video_whisper_emb).astype('float32')

            score_clip = util.cos_sim(video_clip_emb.reshape(1, -1), clip_emb.reshape(1, -1))[0][0]
            score_ocr = util.cos_sim(video_ocr_emb.reshape(1, -1), text_emb.reshape(1, -1))[0][0]
            score_whisper = util.cos_sim(video_whisper_emb.reshape(1, -1), text_emb.reshape(1, -1))[0][0]

            clip_weight, ocr_weight, whisper_weight = self.get_weights(word_whisper_count, word_ocr_count)

            total_score = score_clip * clip_weight + score_ocr * ocr_weight + score_whisper * whisper_weight

            best_videos.append((total_score, id_))

        best_videos.sort(reverse=True, key=lambda x: x[0])

        res = [int(x[1]) for x in best_videos[:k]]
        return res


class ClusterSearcher():
    def __init__(self):
        self.known_updated = 0
        self.load_from_db()

    def load_from_db(self):
        ctime = time()
        if ctime - self.known_updated > 7200:
            with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
                self.clusters = client.query_df(f'SELECT id, mean_emb FROM clusters_embeddings')
            self.clusters['mean_emb'] = self.clusters['mean_emb'].apply(lambda emb: np.array(emb))
            self.known_updated = ctime

    def define_cluster(self, clip_emb):
        clip_emb = np.array(clip_emb, dtype='float64')  # CLIP-эмбеддинг поступившего видео
        self.clusters['sim'] = self.clusters['mean_emb'].apply(
            lambda emb: cosine_similarity(emb.reshape(1, -1), clip_emb.reshape(1, -1))[0][0])
        self.clusters = self.clusters.sort_values(by='sim', ascending=False)
        return self.clusters.head(1).id.tolist()[0]


class AutocompleteService:
    def __init__(self):
        self.phrases_dict = self.get_dict()
        self.autocomplete = AutoComplete(
            words=self.phrases_dict,
            autocomplete = AutoComplete(words=phrases_dict,
                                valid_chars_for_string='абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        )

    def get_n_candidates(self, user_phrase):
        return self.autocomplete.search(word=user_phrase, max_cost=5, size=6)

    def get_dict(self):
        with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
            result = client.query('SELECT word FROM dictionary')
        dict_words = [row[0] for row in result.result_rows]
        return {phrase: {} for phrase in dict_words}

    def clastering_req(self, request):
        candidates_words = self.get_n_candidates(request)
        if not candidates_words:
            return [], []

        list_candidates = [word for sublist in candidates_words for word in sublist]
        list_embeddings = [
            requests.get(TEXTEMBEDDER_URL + '/build_embeddings', json={'text': word}).json()['embeddings']
            for word in list_candidates]
        list_embeddings = np.array(list_embeddings).reshape(len(list_candidates), -1).tolist()

        if len(list_candidates) == 1:
            return list_embeddings, list_candidates

        clustering = AgglomerativeClustering(
            n_clusters=None, distance_threshold=0.2, metric='cosine', linkage='average'
        ).fit(list_embeddings)
        labels = clustering.fit_predict(list_embeddings)

        sort_cand = [list_candidates[i] for i in range(len(labels)) if labels[i] == 0]
        sort_emb = [list_embeddings[i] for i in range(len(labels)) if labels[i] == 0]

        return sort_emb, sort_cand

    def personality(self, sort_emb_list, sort_cand_list):
        with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
            result = client.query('SELECT user_requests FROM users')
        user_requests = [row[0] for row in result.result_rows]

        cos_sim = {
            "word": [],
            "rank": []
        }

        for emb, word in zip(sort_emb_list, sort_cand_list):
            for user_request in user_requests:
                similarity = util.cos_sim(emb, user_request).cpu().numpy().tolist()[0][0]
                cos_sim['word'].append(word)
                cos_sim['rank'].append(similarity)

        df = pd.DataFrame(cos_sim)
        df_sorted = df.sort_values(by='rank', ascending=False)
        df_unique = df_sorted.drop_duplicates(subset='word', keep='first')

        return df_unique.to_dict(orient='list')

    def get_answer(self, request):
        try:
            sort_emb_list, sort_cand_list = self.clastering_req(request)
            if sort_emb_list and sort_cand_list:
                return self.personality(sort_emb_list, sort_cand_list)['word']
            return [request]
        except IndexError:
            return [request]


app = FastAPI()

ranker = SimilarityRanker()
cluster_searcher = ClusterSearcher()
autocompl = AutocompleteService()


@app.get("/")
def base():
    return "Ok"


@app.get("/search")
def findtop(data: dict):
    response = {'videos': ranker.find_top_k(data['text'], k=data['top-k'])}
    return response


@app.post("/define_cluster")
def get_cluster(data: dict):
    cluster_id = cluster_searcher.define_cluster(data['embeddings'])
    with Session(engine) as pg_session:
        video = pg_session.query(Video).filter_by(clickhouse_id=data['ch_video_id']).first()
        cluster = pg_session.query(Cluster).filter_by(id=cluster_id + 1).first()
        cluster.videos.append(video)
        pg_session.add(cluster)
        pg_session.add(video)
        pg_session.commit()

    return 'ok'


@app.get('/search_suggest')
async def search_suggest(data: dict):
    return autocompl.get_answer(data['text'])
