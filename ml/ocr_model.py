import easyocr
import cv2
import torch
import torch.multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

from ml.translator_model import MarianTranslator


class OCRModel:
    def __init__(self):
        if torch.cuda.is_available():
            mp.set_start_method('spawn', force=True)

        self.flag = torch.cuda.is_available()
        self.reader = easyocr.Reader(['en', 'ru'], gpu=self.flag)
        self.translator = MarianTranslator()

    def process_frame(self, frame):
        frame_resized = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        outs = self.reader.readtext(frame_resized)
        outs = [x[1] for x in outs if x[2] >= 0.5]
        outs = ['' if x is None else x for x in outs]
        return ' '.join(outs) if len(outs) > 0 else ''

    def get_text_from_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(frame_rate) * 3
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                frames.append(frame)
            frame_count += 1

        cap.release()

        all_outs = []
        with ThreadPoolExecutor() as executor:
            all_outs = list(executor.map(self.process_frame, frames))

        try:
            fin_text = all_outs[0].capitalize()
            for nt in all_outs[1:]:
                for s in range(min([50, len(nt)]), 1, -1):
                    css = nt[:s]
                    if css in fin_text and s > 3:
                        if len(fin_text) - fin_text.rfind(css) - len(css) < 4:
                            fin_text = fin_text[:fin_text.rfind(css)]
                            break
                fin_text += '. ' + nt.capitalize()
        except Exception as e:
            fin_text = ''

        return self.translator.translate(fin_text)
