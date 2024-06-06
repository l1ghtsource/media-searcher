from ml.text2clip_model import Text2CLIPModel
from ml.text2minilm_model import Text2MiniLM
from sentence_transformers import util


class SimilarityRanker:
    def __init__(self, db):
        self.cliptext = Text2CLIPModel()
        self.textembedder = Text2MiniLM()
        self.db = db

    def get_weights(self, word_whisper_count, word_ocr_count):  # придумать норм формулу для весов

        ocr_weight = 0.2
        whisper_weight = 0.2
        clip_weight = 0.6

        return clip_weight, ocr_weight, whisper_weight

    def find_top_k(self, text, k=5):  # переписать на faiss + потыкаться в претрейн реранкеры
        text_emb = self.textembedder.get_lm_embedding(text).cpu().flatten().detach().numpy()
        clip_emb = self.cliptext.get_text_embedding(text)

        best_videos = []
        for i in range(len(self.db)):
            url, video_clip_emb, video_ocr_emb, video_whisper_emb, word_whisper_count, word_ocr_count = self.db.iloc[i]

            score_clip = util.cos_sim(video_clip_emb, clip_emb).numpy()[0][0]
            score_ocr = util.cos_sim(video_ocr_emb, text_emb).numpy()[0][0]
            score_whisper = util.cos_sim(video_whisper_emb, text_emb).numpy()[0][0]

            clip_weight, ocr_weight, whisper_weight = self.get_weights(word_whisper_count, word_ocr_count)

            total_score = score_clip * clip_weight + score_ocr * ocr_weight + score_whisper * whisper_weight

            best_videos.append((total_score, url))

        best_videos.sort(reverse=True)

        return best_videos[:k]
