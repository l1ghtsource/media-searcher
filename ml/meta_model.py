import torch.multiprocessing as mp
import concurrent.futures

from ml.whisper_model import WhisperModel
from ml.ocr_model import OCRModel
from ml.clip_model import CLIPmodel
from ml.text2minilm_model import Text2MiniLM

mp.set_start_method('spawn', force=True)


class MetaModel:
    def __init__(self):
        self.whisper = WhisperModel()
        self.ocr = OCRModel()
        self.clipvision = CLIPmodel()
        self.textembedder = Text2MiniLM()

    def get_ocr_embeddings(self, video):
        ocr_text = self.ocr.get_text_from_video(video)[:77]
        ocr_emb = self.textembedder.get_lm_embedding(ocr_text).cpu().flatten().detach().numpy()
        return ocr_emb, len(ocr_text)

    def get_whisper_embeddings(self, video):
        whisper_text = self.whisper.process_sample(video)[:77]
        whisper_emb = self.textembedder.get_lm_embedding(whisper_text).cpu().flatten().detach().numpy()
        return whisper_emb, len(whisper_text)

    def get_clip_embeddings(self, video):
        clip_emb = self.clipvision.get_video_embeddings(video).cpu().flatten().detach().numpy()
        return clip_emb

    def get_embeddings(self, video):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_ocr = executor.submit(self.get_ocr_embeddings, video)
            future_whisper = executor.submit(self.get_whisper_embeddings, video)
            future_clip = executor.submit(self.get_clip_embeddings, video)

            for future in concurrent.futures.as_completed([future_ocr, future_whisper, future_clip]):
                if future == future_ocr:
                    ocr_emb, ocr_len = future.result()
                elif future == future_whisper:
                    whisper_emb, whisper_len = future.result()
                elif future == future_clip:
                    clip_emb = future.result()

        return clip_emb, ocr_emb, whisper_emb, whisper_len, ocr_len
