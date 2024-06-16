FROM python:3.11-slim

RUN apt-get update
RUN apt-get install make cmake g++ gcc zlib1g ffmpeg -y
RUN python3 -m pip install --upgrade pip
RUN pip install face_recognition

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN mkdir videos
COPY . . 

CMD ["faststream", "run", "main:app", "--workers", "1"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]