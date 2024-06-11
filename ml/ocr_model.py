import easyocr
import cv2
import torch
from ml.translator_model import MarianTranslator


class OCRModel:
    def __init__(self):
        '''
        Initializes the OCRModel class.

        This method sets up the GPU flag based on availability, initializes the EasyOCR reader for English and Russian languages, 
        and sets up the Google Translator for translating detected text to English.
        '''
        self.flag = True if torch.cuda.is_available() else False
        self.reader = easyocr.Reader(['en', 'ru'], gpu=self.flag)
        self.translator = MarianTranslator()

    def get_text_from_video(self, video_path):
        '''
        Extracts text from the video and translates it to English.

        Args:
            video_path (str): Path to the video file.

        Returns:
            str: The extracted and translated text from the video.
        '''
        cap = cv2.VideoCapture(video_path)

        frames = []
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(frame_rate) * 3  # every 3 seconds
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
        for frame in frames:
            outs = self.reader.readtext(frame)
            outs = [self.translator.translate(x[1]) for x in outs if x[2] >= 0.5]
            outs = ['' if x is None else x for x in outs]
            all_outs.append(' '.join(outs) if len(outs) > 0 else '')

        try:
            fin_text = all_outs[0]
            for nt in all_outs[1:]:
                for s in range(min([10, len(nt)]), 1, -1):
                    css = nt[:s]
                    if css in fin_text and s > 3:
                        if len(fin_text) - fin_text.rfind(css) - len(css) < 4:
                            fin_text = fin_text[:fin_text.rfind(css)]
                            break
                fin_text += '\n' + nt
        except:
            fin_text = ''

        return fin_text
