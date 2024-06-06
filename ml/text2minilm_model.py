import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer


class Text2MiniLM:
    def __init__(self):
        '''
        Initializes the Text2MiniLM class.

        This method sets up the device (GPU if available, otherwise CPU), loads the pretrained MiniLM model and tokenizer.
        '''
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2').to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    def mean_pooling(self, model_output, attention_mask):
        '''
        Applies mean pooling to the token embeddings to obtain sentence embeddings.

        Args:
            model_output (torch.Tensor): The output tensor from the model.
            attention_mask (torch.Tensor): The attention mask tensor.

        Returns:
            torch.Tensor: The sentence embeddings obtained by mean pooling.
        '''
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_lm_embedding(self, text):
        '''
        Computes the sentence embeddings for the input text using the MiniLM model.

        Args:
            text (str): The input text to be embedded.

        Returns:
            torch.Tensor: A tensor containing the normalized sentence embeddings (size 384).
        '''
        encoded_input = self.tokenizer([text], padding=True, truncation=True, return_tensors='pt').to(self.device)

        with torch.no_grad():
            model_output = self.model(**encoded_input)

        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        return sentence_embeddings
