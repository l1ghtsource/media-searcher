import concurrent.futures
import torch
import torch.multiprocessing as mp

from ml.whisper_model import WhisperModel
from ml.ocr_model import OCRModel
from ml.clip_model import CLIPmodel
from ml.text2minilm_model import Text2MiniLM


class MetaModel:
    def __init__(self):
        self.whisper = WhisperModel()
        self.ocr = OCRModel()
        self.clipvision = CLIPmodel()
        self.textembedder = Text2MiniLM()

        if torch.cuda.is_available():
            mp.set_start_method('spawn', force=True)

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
            future_to_method = {
                executor.submit(self.get_ocr_embeddings, video): 'ocr',
                executor.submit(self.get_whisper_embeddings, video): 'whisper',
                executor.submit(self.get_clip_embeddings, video): 'clip'
            }

            results = {}
            for future in concurrent.futures.as_completed(future_to_method):
                method = future_to_method[future]
                try:
                    result = future.result()
                    results[method] = result
                except Exception as exc:
                    print(f'{method} generated an exception: {exc}')

        clip_emb = results['clip']
        ocr_emb, ocr_len = results['ocr']
        whisper_emb, whisper_len = results['whisper']

        return clip_emb, ocr_emb, whisper_emb, whisper_len, ocr_len
