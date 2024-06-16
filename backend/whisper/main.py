from models import Base, Face, Video
import os
import shutil
import subprocess
import requests

import clickhouse_connect
from faststream import FastStream
from faststream.kafka import KafkaBroker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import torch
import torchaudio
from torchaudio.transforms import Resample
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor


TRANSLATOR_URL = os.environ['TRANSLATOR_URL']
TEXTEMBEDDER_URL = os.environ['TEXTEMBEDDER_URL']

CLICKHOUSE_HOST = os.environ['CLICKHOUSE_HOST']
CLICKHOUSE_USERNAME = os.environ['CLICKHOUSE_USERNAME']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']

WHISPER_MODEL = os.environ.get('WHISPER_MODEL', 'whisper_base')  # '/whisper_medium'

POSTGRES_URL = os.environ['POSTGRES_URL']

KAFKA_URL = os.environ['KAFKA_URL']


def download_models():
    if len(os.listdir("/whisper_medium")) == 0:
        model = AutoModelForSpeechSeq2Seq.from_pretrained('openai/whisper-medium')
        model.save_pretrained("/whisper_medium")
        processor = AutoProcessor.from_pretrained('openai/whisper-medium')
        processor.save_pretrained("/whisper_medium")

    if len(os.listdir("/whisper_base")) == 0:
        model = AutoModelForSpeechSeq2Seq.from_pretrained('openai/whisper-base')
        model.save_pretrained("/whisper_base")
        processor = AutoProcessor.from_pretrained('openai/whisper-base')
        processor.save_pretrained("/whisper_base")


download_models()


class WhisperModel():
    def __init__(self):
        self.model_id = '/' + WHISPER_MODEL
        self.dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(self.model_id, torch_dtype=self.dtype,
                                                               low_cpu_mem_usage=True, use_safetensors=True
                                                               ).to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.model_id)
        self.forced_decoder_ids_eng = self.processor.get_decoder_prompt_ids(language='english', task='transcribe')
        self.forced_decoder_ids = self.processor.get_decoder_prompt_ids(task='transcribe')
        self.resampler = {}
        self.vad, self.vad_utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                                  model='silero_vad',
                                                  force_reload=False,
                                                  onnx=True)

    def process_sample(self, filename):

        try:
            code = subprocess.call(
                [
                    'ffmpeg',
                    '-y',
                    '-i',
                    filename,
                    '-vn',
                    '/tmp/audio.wav'
                ],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )

            if code != 0:
                raise ValueError()

            clip, clip_hz = torchaudio.load('/tmp/audio.wav', backend='ffmpeg')

        except:
            return ''

        if clip_hz != 16000:

            if clip_hz not in self.resampler:
                self.resampler[clip_hz] = Resample(clip_hz, 16000)
            clip = self.resampler[clip_hz](clip)

        clip = clip.mean(dim=0)  # stereo to mono
        speech_ts = self.vad_utils[0](clip.unsqueeze(0), self.vad, sampling_rate=16000, threshold=0.1)

        full_eng = []
        full = []
        for ts in speech_ts:

            with torch.inference_mode():
                input_features = self.processor(
                    clip[ts['start']:ts['end'] + 1], sampling_rate=16000, return_tensors='pt'
                ).input_features.to(self.dtype).to(self.device)

                predicted_ids_eng = self.model.generate(input_features,
                                                        forced_decoder_ids=self.forced_decoder_ids_eng,
                                                        do_sample=True,
                                                        temperature=0.3)
                transcription_eng = self.processor.batch_decode(predicted_ids_eng, skip_special_tokens=True)

                full_eng.append(transcription_eng[0])

                predicted_ids = self.model.generate(input_features,
                                                    forced_decoder_ids=self.forced_decoder_ids,
                                                    do_sample=True,
                                                    temperature=0.3)
                transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)

                full.append(transcription[0])

        return ' '.join(full_eng), ' '.join(full)


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


def push_data(ch_video_id, embeddings, text_len, readed_text):
    with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
        client.query(
            f'ALTER TABLE embeddings UPDATE whisper_emb = {embeddings}, whisper_len = {text_len}  WHERE id = {ch_video_id}')

    with Session(engine) as session:
        video = session.query(Video).filter_by(clickhouse_id=ch_video_id).first()
        video.speech_text = readed_text
        session.add(video)
        session.commit()


def build_embeddings(text):
    return requests.get(TEXTEMBEDDER_URL + '/build_embeddings', json={'text': text}).json()['embeddings']


def translate_text(text):
    return requests.get(TRANSLATOR_URL + '/translate', json={'text': text}).json()['translation']


broker = KafkaBroker(KAFKA_URL)
whisper = WhisperModel()
engine = create_engine(POSTGRES_URL, pool_pre_ping=True)


@broker.subscriber("new_video_whisper")
async def base_handler(body):
    ch_video_id = body['ch_video_id']
    s3_url = body['s3_url']

    path = get_video(ch_video_id, s3_url)
    english_text, text = whisper.process_sample(path)
    embs = build_embeddings(english_text)

    push_data(ch_video_id, embs, len(english_text), text)

app = FastStream(broker,  description="Whisper")
