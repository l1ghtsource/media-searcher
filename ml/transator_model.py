import torch
from transformers import MarianMTModel, MarianTokenizer


class MarianTranslator:
    '''
    A class for translating text using the Marian model.

    Attributes:
        device (str): The device to run the model on ('cuda' if GPU is available, otherwise 'cpu').
        model (MBartForConditionalGeneration): The Marian model for text generation.
        tokenizer (MBart50TokenizerFast): The tokenizer for the MBart model.
    '''

    def __init__(self):
        '''
        Initializes the Translator with the MBart model and tokenizer, source language is Russian.
        '''
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = MarianMTModel.from_pretrained('lightsource/yappy-fine-tuned-opus-mt-ru-en').to(self.device)
        self.tokenizer = MarianTokenizer.from_pretrained('lightsource/yappy-fine-tuned-opus-mt-ru-en')

    def translate(self, text):
        '''
        Translates the given text to the English.

        Args:
            text (str): The input text to be translated.

        Returns:
            list: The translated text.
        '''
        inputs = self.tokenizer(text, return_tensors='pt', padding=True).to(self.device)
        translated = self.model.generate(**inputs)

        translated_text = [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]

        return translated_text[0]
