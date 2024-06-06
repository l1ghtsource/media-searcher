import torch
from transformers import CLIPTextModelWithProjection, CLIPTokenizer


class Text2CLIPModel:
    def __init__(self):
        '''
        Initializes the Text2CLIPModel class.

        This method sets up the device (GPU if available, otherwise CPU), loads the pretrained CLIP text model and tokenizer.
        '''
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = CLIPTextModelWithProjection.from_pretrained('Searchium-ai/clip4clip-webvid150k').to(self.device)
        self.tokenizer = CLIPTokenizer.from_pretrained('Searchium-ai/clip4clip-webvid150k')

    def get_text_embedding(self, text):
        '''
        Computes the text embeddings using the CLIP model.

        Args:
            text (str): The input text to be embedded.

        Returns:
            numpy.ndarray: A numpy array containing the normalized text embeddings (size 512).
        '''
        inputs = self.tokenizer(text=text, return_tensors='pt').to(self.device)
        outputs = self.model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])
        final_output = outputs[0] / outputs[0].norm(dim=-1, keepdim=True)
        final_output = final_output.cpu().detach().numpy()

        return final_output
