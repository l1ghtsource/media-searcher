FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

#RUN apt-get update
#RUN apt-get install make cmake g++ gcc zlib1g ffmpeg -y
RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install faiss-cpu
COPY . . 

#CMD ["python3", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]