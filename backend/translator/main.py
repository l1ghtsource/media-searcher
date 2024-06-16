import os
import torch
from transformers import MarianMTModel, MarianTokenizer
from fastapi import FastAPI

def download_models():
    if len(os.listdir("/opus_model")) == 0:
        model = MarianMTModel.from_pretrained('lightsource/yappy-fine-tuned-opus-mt-ru-en')
        tokenizer = MarianTokenizer.from_pretrained('lightsource/yappy-fine-tuned-opus-mt-ru-en')
        tokenizer.save_pretrained("/opus_model")
        model.save_pretrained("/opus_model")
download_models()

class MarianTranslator:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = MarianMTModel.from_pretrained('/opus_model').to(self.device)
        self.tokenizer = MarianTokenizer.from_pretrained('/opus_model')

    def translate(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True).to(self.device)
        translated = self.model.generate(**inputs)

        translated_text = [self.tokenizer.decode(t, skip_special_tokens=True, truncation=True) for t in translated]

        return translated_text[0]

translator = MarianTranslator()


app = FastAPI()

@app.get("/")
def base():
    return "Ok"

@app.get("/translate")
def translate(data: dict):
    response = {'translation': translator.translate(data['text'])}
    return response