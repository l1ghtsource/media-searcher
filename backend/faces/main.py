import os
import shutil
from time import time
import requests
import cv2
import face_recognition
import numpy as np
import clickhouse_connect
from faststream import FastStream
from faststream.kafka import KafkaBroker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Face, Video


CLICKHOUSE_HOST = os.environ['CLICKHOUSE_HOST']
CLICKHOUSE_USERNAME = os.environ['CLICKHOUSE_USERNAME']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']

KAFKA_URL = os.environ['KAFKA_URL']

POSTGRES_URL = os.environ['POSTGRES_URL']
engine = create_engine(POSTGRES_URL, pool_pre_ping=True)


class FaceFounder():
    def __init__(self):
        self.known_embs_updated = 0
        self.check_known()

    def get_frames(self, fp):
        with open(fp, 'rb') as f:
            print(f.read()[:21])

        cap = cv2.VideoCapture(fp)
        success, frame = cap.read()

        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        total_duration = (frameCount + fps - 1) // fps

        frame_interval = max([2, total_duration / 6])

        images = []
        count = 0

        while success:
            if count % int(frame_interval * fps) == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                images.append(frame)
            success, frame = cap.read()
            count += 1
        cap.release()

        return images

    def get_unique(self, images, video_id):

        face_locations = [face_recognition.face_locations(img) for img in images]
        face_encodings = []
        for i in range(len(images)):
            for f in face_recognition.face_encodings(images[i], face_locations[i]):
                face_encodings.append(f)

        diff_encodings = []
        enc_counter = []
        for e in face_encodings:
            found = False
            mask = face_recognition.compare_faces(diff_encodings, e)
            if True not in mask:
                diff_encodings.append(e)
                enc_counter.append(1)
            else:
                ind = mask.index(True)
                diff_encodings[ind] += e
                diff_encodings[ind] /= 2
                enc_counter[ind] += 1

        enc_pairs = [[diff_encodings[i], enc_counter[i]] for i in range(len(enc_counter))]
        enc_pairs.sort(key=lambda x: x[1])
        data = []
        for i, enc in enumerate(reversed(enc_pairs)):
            data.append([video_id, enc[0], i])

        return data

    def check_known(self):
        ctime = time()
        if ctime - self.known_embs_updated > 7200:
            with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
                self.known_embs = list(client.query(f'SELECT id, face_emb FROM known_faces_embeddings').result_rows)

            for i in range(len(self.known_embs)):
                self.known_embs[i] = [self.known_embs[i][0], np.array(self.known_embs[i][1])]
            self.known_embs_updated = ctime

    def find_known(self, data):
        self.check_known()
        embs = [np.array(i[1]) for i in data]
        known_uuids = []
        for uuid, k_emb in self.known_embs:
            mask = face_recognition.compare_faces(embs, k_emb)
            for i, flag in enumerate(mask):
                if flag:
                    known_uuids.append(uuid)
        return known_uuids

    def process_file(self, fp, vid):
        images = self.get_frames(fp)
        data = self.get_unique(images, vid)
        known_uuids = self.find_known(data)
        return data, known_uuids


def push_data(data, known_uuids, vid):
    with Session(engine) as pg_session:
        video = pg_session.query(Video).filter_by(clickhouse_id=vid).first()
        for uuid in known_uuids:
            face = pg_session.query(Face).filter_by(embedding_uuid=uuid).first()
            video.faces.append(face)
            pg_session.add(face)
            pg_session.add(video)
        pg_session.commit()
    with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
        client.insert("faces_embeddings", data, column_names=['id', 'face_emb', 'rank'])


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


ff = FaceFounder()
broker = KafkaBroker(KAFKA_URL)


@broker.subscriber("new_video_facefounder")
async def base_handler(body):
    ch_video_id = body['ch_video_id']
    s3_url = body['s3_url']

    path = get_video(ch_video_id, s3_url)
    data, known_uuids = ff.process_file(path, ch_video_id)
    push_data(data, known_uuids, ch_video_id)

app = FastStream(broker,  description="FaceFounder")
