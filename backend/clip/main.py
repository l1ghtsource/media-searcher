import os
import shutil
import cv2
import requests
import numpy as np

import clickhouse_connect
from faststream import FastStream
from faststream.kafka import KafkaBroker
from PIL import Image
import torch
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize, InterpolationMode

from transformers import AutoProcessor
from transformers import CLIPVisionModelWithProjection


CLICKHOUSE_HOST = os.environ['CLICKHOUSE_HOST']
CLICKHOUSE_USERNAME = os.environ['CLICKHOUSE_USERNAME']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']
SEARCH_URL = os.environ['SEARCH_URL']
if SEARCH_URL == '':
    print(SEARCH_URL)
    quit()

KAFKA_URL = os.environ['KAFKA_URL']


def download_models():
    if len(os.listdir("/clip_model")) == 0:
        model = CLIPVisionModelWithProjection.from_pretrained("Searchium-ai/clip4clip-webvid150k")
        model.save_pretrained("/clip_model")
        processor = AutoProcessor.from_pretrained("Searchium-ai/clip4clip-webvid150k")
        processor.save_pretrained("/clip_model")


download_models()


class CLIPmodel:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPVisionModelWithProjection.from_pretrained("/clip_model").to(self.device)
        self.processor = AutoProcessor.from_pretrained("/clip_model")

    def video2image(self, video_path, frame_rate=1.0, size=224):
        def preprocess(size, n_px):
            return Compose([
                Resize(size, interpolation=InterpolationMode.BICUBIC),
                CenterCrop(size),
                lambda image: image.convert("RGB"),
                ToTensor(),
                Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
            ])(n_px)

        cap = cv2.VideoCapture(video_path)
        cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        if fps < 1:
            images = np.zeros([3, size, size], dtype=np.float32)
            print("ERROR: problem reading video file: ", video_path)
        else:
            total_duration = (frameCount + fps - 1) // fps
            start_sec, end_sec = 0, total_duration
            interval = fps / frame_rate
            frames_idx = np.floor(np.arange(start_sec*fps, end_sec*fps, interval))
            ret = True
            images = np.zeros([len(frames_idx), 3, size, size], dtype=np.float32)

            for i, idx in enumerate(frames_idx):
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                last_frame = i
                images[i, :, :, :] = preprocess(size, Image.fromarray(frame).convert("RGB"))

            images = images[:last_frame+1]
        cap.release()
        video_frames = torch.tensor(images)

        return video_frames

    def get_video_embeddings(self, path):
        self.model = self.model.eval()

        video = self.video2image(path).to(self.device)
        visual_output = self.model(video)

        visual_output = visual_output["image_embeds"]
        visual_output = visual_output / visual_output.norm(dim=-1, keepdim=True)
        visual_output = torch.mean(visual_output, dim=0)
        visual_output = visual_output / visual_output.norm(dim=-1, keepdim=True)

        return visual_output.cpu().flatten().detach().tolist()


clip = CLIPmodel()


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


def push_data(ch_video_id, embeddings):
    with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
        client.query(f'ALTER TABLE embeddings UPDATE clip_emb = {embeddings}  WHERE id = {ch_video_id}')


broker = KafkaBroker(KAFKA_URL)


@broker.subscriber("new_video_clip")
async def base_handler(body):
    ch_video_id = body['ch_video_id']
    s3_url = body['s3_url']

    path = get_video(ch_video_id, s3_url)

    embs = clip.get_video_embeddings(path)

    push_data(ch_video_id, embs)
    requests.post(SEARCH_URL + '/define_cluster', json={'embeddings': embs, 'ch_video_id': ch_video_id})


app = FastStream(broker, description="CLIP")
