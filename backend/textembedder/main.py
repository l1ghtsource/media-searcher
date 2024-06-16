import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI



def download_models():
    if len(os.listdir("/minilm")) == 0:
        model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
        tokenizer.save_pretrained("/minilm")
        model.save_pretrained("/minilm")
download_models()

class Text2MiniLM:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = AutoModel.from_pretrained('/minilm', local_files_only=True).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained('/minilm', local_files_only=True)
        
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def get_lm_embedding(self, text):
        encoded_input = self.tokenizer([text], padding=True, truncation=True, return_tensors='pt').to(self.device)

        with torch.no_grad():
            model_output = self.model(**encoded_input)

        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        
        return sentence_embeddings.cpu().flatten().detach().tolist()

Text2Mini = Text2MiniLM()

app = FastAPI()

@app.get("/")
def base():
    return "Ok"

@app.get("/build_embeddings")
def build_embeddings(text: dict):
    response = {'embeddings': Text2Mini.get_lm_embedding(text['text'])}
    return response