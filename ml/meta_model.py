import concurrent.futures
import torch
import torch.multiprocessing as mp

from ml.whisper_model import WhisperModel
from ml.ocr_model import OCRModel
from ml.clip_model import CLIPmodel
from ml.text2minilm_model import Text2MiniLM


class MetaModel:
    def __init__(self):
        '''
        Initializes the MetaModel class.

        This method sets up the Whisper, OCR, CLIP vision, and Text2MiniLM models.
        '''
        if torch.cuda.is_available():  # for multiprocessing on GPU
            mp.set_start_method('spawn', force=True)

        self.whisper = WhisperModel()
        self.ocr = OCRModel()
        self.clipvision = CLIPmodel()
        self.textembedder = Text2MiniLM()

    def get_ocr_embeddings(self, video):
        '''
        Extracts text from the video using OCR, then computes the text embeddings.

        Args:
            video (str): Path to the video file.

        Returns:
            tuple: A tuple containing the OCR text embeddings as a numpy array and the length of the OCR text.
        '''
        ocr_text = self.ocr.get_text_from_video(video)[:77]
        ocr_emb = self.textembedder.get_lm_embedding(ocr_text).cpu().flatten().detach().numpy()
        return ocr_emb, len(ocr_text)

    def get_whisper_embeddings(self, video):
        '''
        Extracts speech from the video using Whisper, then computes the text embeddings.

        Args:
            video (str): Path to the video file.

        Returns:
            tuple: A tuple containing the Whisper text embeddings as a numpy array and the length of the Whisper text.
        '''
        whisper_text = self.whisper.process_sample(video)[:77]
        whisper_emb = self.textembedder.get_lm_embedding(whisper_text).cpu().flatten().detach().numpy()
        return whisper_emb, len(whisper_text)

    def get_clip_embeddings(self, video):
        '''
        Computes the CLIP embeddings for the video.

        Args:
            video (str): Path to the video file.

        Returns:
            numpy.ndarray: A numpy array containing the CLIP video embeddings.
        '''
        clip_emb = self.clipvision.get_video_embeddings(video).cpu().flatten().detach().numpy()
        return clip_emb

    def get_embeddings(self, video):
        '''
        Computes the OCR, Whisper, and CLIP embeddings for the video concurrently.

        Args:
            video (str): Path to the video file.

        Returns:
            tuple: A tuple containing the CLIP, OCR, and Whisper embeddings as numpy arrays, and the lengths of the Whisper and OCR texts.
        '''
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
