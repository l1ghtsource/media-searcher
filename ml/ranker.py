import faiss
import numpy as np
import pandas as pd
from deep_translator import GoogleTranslator
from sentence_transformers import util

from ml.text2clip_model import Text2CLIPModel
from ml.text2minilm_model import Text2MiniLM


class SimilarityRanker:
    '''
    A class to rank the similarity of videos based on text input using various embeddings and similarity scores.

    Attributes:
        db (pd.DataFrame): DataFrame containing video embeddings and other metadata.
        df (pd.DataFrame): DataFrame containing video links and additional information.
        cliptext (Text2CLIPModel): Model for generating CLIP text embeddings.
        textembedder (Text2MiniLM): Model for generating MiniLM text embeddings.
        translator (GoogleTranslator): Translator for translating text to English.
        index_clip (faiss.IndexFlatL2): FAISS index for CLIP embeddings.
        index_ocr (faiss.IndexFlatL2): FAISS index for OCR embeddings.
        index_whisper (faiss.IndexFlatL2): FAISS index for Whisper embeddings.
    '''

    def __init__(self, db, df):
        '''
        Initializes the SimilarityRanker with embeddings, translators, and FAISS indices.

        Args:
            db (pd.DataFrame): DataFrame containing video embeddings and other metadata.
            df (pd.DataFrame): DataFrame containing video links and additional information.
        '''
        self.cliptext = Text2CLIPModel()
        self.textembedder = Text2MiniLM()
        self.translator = GoogleTranslator(source='auto', target='en')
        self.db = db
        self.df = df
        self.index_clip = self.create_faiss_index(np.vstack(self.db['clip_emb'].values).astype('float32'))
        self.index_ocr = self.create_faiss_index(np.vstack(self.db['ocr_emb'].values).astype('float32'))
        self.index_whisper = self.create_faiss_index(np.vstack(self.db['whisper_emb'].values).astype('float32'))

    def create_faiss_index(self, embeddings):
        '''
        Creates a FAISS index for the given embeddings.

        Args:
            embeddings (np.ndarray): Array of embeddings to be indexed.

        Returns:
            faiss.IndexFlatL2: A FAISS index of the embeddings.
        '''
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index

    def get_weights(self, word_whisper_count, word_ocr_count):
        '''
        Computes weights for the different embedding types.

        Args:
            word_whisper_count (int): Count of words from the Whisper model.
            word_ocr_count (int): Count of words from the OCR model.

        Returns:
            tuple: Weights for clip, ocr, and whisper embeddings.
        '''
        max_count = 77

        w_1 = (word_ocr_count / (max_count + word_ocr_count))
        w_2 = (word_whisper_count / (max_count + word_whisper_count))

        ocr_weight = 0.05 * w_1
        whisper_weight = 0.05 * w_2
        clip_weight = 0.9 * (1 - (w_1 + w_2) / 2)

        ocr_weight, whisper_weight, clip_weight = np.exp(
            [ocr_weight, whisper_weight, clip_weight]) / np.sum(np.exp([ocr_weight, whisper_weight, clip_weight]))

        return clip_weight, ocr_weight, whisper_weight

    def find_top_k(self, text, k=10):
        '''
        Finds the top k videos that are most similar to the given text.

        Args:
            text (str): The input text to find similar videos for.
            k (int): The number of top similar videos to return.

        Returns:
            dict: A dictionary with similarity scores as keys and video links as values.
        '''
        text = self.translator.translate(text)

        text_emb = self.textembedder.get_lm_embedding(text).cpu().flatten().detach().numpy()
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

        res = {x[0].item(): self.df.iloc[x[1]].link for x in best_videos[:k]}

        return res


# import clickhouse_connect

# client = clickhouse_connect.get_client(host='91.224.86.248', port=8123)
# TABLENAME = 'embeddings'

# data = client.query_df(f'SELECT id, clip_emb, ocr_emb, whisper_emb, whisper_len, ocr_len FROM {TABLENAME}')
# data = data.drop_duplicates(subset='id')

# df = pd.read_csv('data\yappy_hackaton_2024_400k.csv')

# ranker = SimilarityRanker(data, df)
# res = ranker.find_top_k('your text', k=10)
