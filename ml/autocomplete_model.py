import numpy as np
import pandas as pd
import clickhouse_connect
from fast_autocomplete import AutoComplete
from sentence_transformers import util
from sklearn.cluster import AgglomerativeClustering
from text2minilm_model import Text2MiniLM


client = clickhouse_connect.get_client(host='91.224.86.248',
                                       port=8123,
                                       username=...,
                                       password=...)


class AutocompleteService:
    def __init__(self, client):
        self.model = Text2MiniLM()
        self.client = client
        self.phrases_dict = self.get_dict()
        self.autocomplete = AutoComplete(
            words=self.phrases_dict,
            valid_chars_for_string='абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        )

    def get_n_candidates(self, user_phrase):
        return self.autocomplete.search(word=user_phrase, max_cost=5, size=6)

    def get_dict(self):
        result = self.client.query('SELECT word FROM dictionary')
        dict_words = [row[0] for row in result.result_rows]
        return {phrase: {} for phrase in dict_words}

    def clastering_req(self, request):
        candidates_words = self.get_n_candidates(request)
        if not candidates_words:
            return [], []

        list_candidates = [word for sublist in candidates_words for word in sublist]
        list_embeddings = [self.model.get_lm_embedding(word).cpu().numpy().tolist() for word in list_candidates]
        list_embeddings = np.array(list_embeddings).reshape(len(list_candidates), -1).tolist()

        if len(list_candidates) == 1:
            return list_embeddings, list_candidates

        clustering = AgglomerativeClustering(
            n_clusters=None, distance_threshold=0.2, affinity='cosine', linkage='average'
        ).fit(list_embeddings)
        labels = clustering.fit_predict(list_embeddings)

        sort_cand = [list_candidates[i] for i in range(len(labels)) if labels[i] == 0]
        sort_emb = [list_embeddings[i] for i in range(len(labels)) if labels[i] == 0]

        return sort_emb, sort_cand

    def personality(self, sort_emb_list, sort_cand_list):
        result = self.client.query('SELECT user_requests FROM users')
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
                return self.personality(sort_emb_list, sort_cand_list)
            return request
        except IndexError:
            return request
