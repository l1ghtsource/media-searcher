import os
import requests
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List
import clickhouse_connect
import boto3
import boto3.session
from faststream.kafka.fastapi import KafkaRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Face, Video, Cluster
from fastapi_models import *


TRANSLATOR_URL = os.environ['TRANSLATOR_URL']
TEXTEMBEDDER_URL = os.environ['TEXTEMBEDDER_URL']
SEARCH_URL = os.environ['SEARCH_URL']


CLICKHOUSE_HOST = os.environ['CLICKHOUSE_HOST']
CLICKHOUSE_USERNAME = os.environ['CLICKHOUSE_USERNAME']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']

POSTGRES_URL = os.environ['POSTGRES_URL']

KAFKA_URL = os.environ['KAFKA_URL']

S3_SECRET = os.environ['S3_SECRET']
S3_PUBLIC = os.environ['S3_PUBLIC']


router = KafkaRouter(KAFKA_URL)

s3_session = boto3.session.Session(
    aws_access_key_id=S3_PUBLIC,
    aws_secret_access_key=S3_SECRET,
    region_name="ru-central-1",
)

app = FastAPI(lifespan=router.lifespan_context,
              description='Документация к api поиска, и обработки видео')
app.include_router(router)

engine = create_engine(POSTGRES_URL, pool_pre_ping=True)
Base.metadata.create_all(bind=engine)

clip_zero = [0 for i in range(4*128)]
ocr_zero = [0 for i in range(96*4)]
whisper_zero = [0 for i in range(96*4)]


@app.get("/get_upload_url")
async def prepare_to_download():
    with Session(engine) as pg_session:
        video = Video()
        pg_session.add(video)
        pg_session.commit()
        video_id = video.id
        video.clickhouse_id = video_id
        video.url = 'https://lct-video-0.storage.yandexcloud.net/' + str(video_id)
        pg_session.commit()

    s3 = s3_session.client(service_name="s3", endpoint_url="https://storage.yandexcloud.net")
    put_url = s3.generate_presigned_url("put_object", Params={"Bucket": 'lct-video-0', "Key": video_id}, ExpiresIn=3600)
    return UploadUrl(url=put_url, id=video_id)


@app.post("/upload_complete")
async def upload_complete(report: UploadCompleteReport):
    report = report.dict()
    video_id = report['id']
    desc = report['description']
    with Session(engine) as pg_session:
        video = pg_session.query(Video).filter_by(id=video_id).first()
        video.description = desc
        url = video.url
        pg_session.add(video)
        pg_session.commit()
    with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
        client.insert('embeddings', [[video_id, clip_zero, ocr_zero, whisper_zero, 0, 0]], column_names=[
                      'id', 'clip_emb', 'ocr_emb', 'whisper_emb', 'whisper_len', 'ocr_len'])

    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_clip")
    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_facefounder")
    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_ocr")
    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_whisper")

    return StartProcessAnswer(id=video_id)


@app.post("/index")
async def upload_complete(data: UploadByUrl):
    data = data.dict()
    url = data['url']
    desc = data['description']
    with Session(engine) as pg_session:
        video = Video()
        pg_session.add(video)
        pg_session.commit()
        video_id = video.id
        video.clickhouse_id = video_id
        video.description = desc
        video.url = url
        pg_session.commit()

    with clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=8123, username=CLICKHOUSE_USERNAME, password=CLICKHOUSE_PASSWORD) as client:
        client.insert('embeddings', [[video_id, clip_zero, ocr_zero, whisper_zero, 0, 0]], column_names=[
                      'id', 'clip_emb', 'ocr_emb', 'whisper_emb', 'whisper_len', 'ocr_len'])

    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_clip")
    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_facefounder")
    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_ocr")
    await router.broker.publish({"ch_video_id": video_id, 's3_url': url}, "new_video_whisper")

    return StartProcessAnswer(id=video_id)


@app.get('/search')
async def search(text: str, number:int=20) -> List[VideoJSON]:
    video_ids = requests.get(SEARCH_URL + '/search', json={'text': text, 'top-k': number}).json()['videos']
    final_data = []
    with Session(engine) as pg_session:
        videos = pg_session.query(Video).filter(Video.clickhouse_id.in_(video_ids)).all()
        for video in videos:
            final_data.append(video.to_json())

    return final_data


@app.get('/search_suggest')
async def search_suggest(text: str) -> List[str]:
    video_ids = requests.get(SEARCH_URL + '/search_suggest', json={'text': text}).json()
    return video_ids


@app.post('/get_cluster_video')
def get_cluster_video(data: IdsList) -> List[VideoJSON]:
    cluster_ids = data.ids
    res = []
    with Session(engine) as pg_session:
        clusters = pg_session.query(Cluster).filter(Cluster.id.in_(cluster_ids)).all()
        for cluster in clusters:
            for video in cluster.videos:
                res.append(video.to_json())
    return res


@app.post('/get_face_video')
def get_face_video(data: IdsList) -> List[VideoJSON]:
    face_ids = data.ids
    res = []
    with Session(engine) as pg_session:
        faces = pg_session.query(Face).filter(Face.id.in_(face_ids)).all()
        for face in faces:
            for video in face.videos:
                res.append(video.to_json())
    return res


@app.get('/get_clusters')
def get_clusters() -> ClustersList:
    res = []
    with Session(engine) as pg_session:
        for c in pg_session.query(Cluster).all():
            res.append({'id': c.id, 'name': c.name})
    return {'title': 'Подборки', 'options': res}


@app.get('/get_faces')
def get_faces() -> FacesList:
    res = []
    with Session(engine) as pg_session:
        for c in pg_session.query(Face).all():
            res.append({'id': c.id, 'name': c.name, 'url': c.image_url})
    return {'title': 'Блогеры', 'options': res}

@app.get('/video')
async def search(video_id: int) -> VideoJSON:
    video_id = int(video_id)
    with Session(engine) as pg_session:
        video = pg_session.filter_by(id=video_id).first()
        final_data = video.to_json()

    return final_data


@app.get('/video_status')
async def video_status(data: dict):
    video_id = data['video_id']
    return ['OCR', 'CLIP', 'FACES', 'WHISPER', 'CLUSTER']
