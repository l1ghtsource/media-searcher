import torch
from transformers import CLIPTextModelWithProjection, CLIPTokenizer


class Text2CLIPModel:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = CLIPTextModelWithProjection.from_pretrained('Searchium-ai/clip4clip-webvid150k').to(self.device)
        self.tokenizer = CLIPTokenizer.from_pretrained('Searchium-ai/clip4clip-webvid150k')

    def get_text_embedding(self, text):
        inputs = self.tokenizer(text=text, return_tensors='pt').to(self.device)
        outputs = self.model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
        final_output = outputs[0] / outputs[0].norm(dim=-1, keepdim=True)
        final_output = final_output.cpu().detach().numpy()

        return final_output
