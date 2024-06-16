FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY . .
#CMD ["python3", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
