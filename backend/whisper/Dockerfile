FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

RUN apt-get update && apt-get install ffmpeg -y
#RUN curl -o /vad.zip https://codeload.github.com/snakers4/silero-vad/legacy.zip/refs/heads/master
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
RUN mkdir videos
COPY . .
CMD ["faststream", "run", "main:app", "--workers", "1"]