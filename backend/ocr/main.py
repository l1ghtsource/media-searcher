import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import requests
import torch
import torch.multiprocessing as mp
import cv2
import easyocr
import clickhouse_connect
from faststream import FastStream
from faststream.kafka import KafkaBroker


TRANSLATOR_URL = os.environ['TRANSLATOR_URL']
TEXTEMBEDDER_URL = os.environ['TEXTEMBEDDER_URL']

CLICKHOUSE_HOST = os.environ['CLICKHOUSE_HOST']
CLICKHOUSE_USERNAME = os.environ['CLICKHOUSE_USERNAME']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']

KAFKA_URL = os.environ['KAFKA_URL']


def download_models():
    pass


if torch.cuda.is_available():
    mp.set_start_method('spawn', force=True)  # для gpu, занимает примерно 2800MB памяти


class OCRModel:
    def __init__(self):
        self.flag = torch.cuda.is_available()
        self.reader = easyocr.Reader(['en', 'ru'], gpu=self.flag,  model_storage_directory='/ocr_models/model')

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
        print(frame_rate)
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
        return fin_text


def get_video(video_id, url):
    if len(os.listdir('videos')) > 10:
        shutil.rmtree('videos')
        os.mkdir('videos')
    fname = f'videos/{video_id}.mp4'

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=16384):
                f.write(chunk)
    return fname


def push_data(ch_video_id, embeddings, text_len):
    with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
        client.query(
            f'ALTER TABLE embeddings UPDATE ocr_emb = {embeddings}, ocr_len = {text_len}  WHERE id = {ch_video_id}')


def build_embeddings(text):
    return requests.get(TEXTEMBEDDER_URL + '/build_embeddings', json={'text': text}).json()['embeddings']


def translate_text(text):
    return requests.get(TRANSLATOR_URL + '/translate', json={'text': text}).json()['translation']


ocr_model = OCRModel()

broker = KafkaBroker(KAFKA_URL)


@broker.subscriber("new_video_ocr")
async def base_handler(body):
    ch_video_id = body['ch_video_id']
    s3_url = body['s3_url']

    path = get_video(ch_video_id, s3_url)
    text = ocr_model.get_text_from_video(path)
    english_text = translate_text(text)
    embs = build_embeddings(english_text)
    push_data(ch_video_id, embs, len(english_text))

app = FastStream(broker,  description="OCR")
