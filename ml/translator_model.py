import torch
from transformers import MarianMTModel, MarianTokenizer


class MarianTranslator:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = MarianMTModel.from_pretrained('lightsource/yappy-fine-tuned-opus-mt-ru-en').to(self.device)
        self.tokenizer = MarianTokenizer.from_pretrained('lightsource/yappy-fine-tuned-opus-mt-ru-en')

    def translate(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True).to(self.device)
        translated = self.model.generate(**inputs)

        translated_text = [self.tokenizer.decode(t, skip_special_tokens=True, truncation=True) for t in translated]

        return translated_text[0]
