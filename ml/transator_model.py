import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


class Translator:
    '''
    A class for translating text using the MBart model.

    Attributes:
        device (str): The device to run the model on ('cuda' if GPU is available, otherwise 'cpu').
        model (MBartForConditionalGeneration): The MBart model for text generation.
        tokenizer (MBart50TokenizerFast): The tokenizer for the MBart model.
    '''

    def __init__(self):
        '''
        Initializes the Translator with the MBart model and tokenizer, setting the default source language to Russian.
        '''
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = MBartForConditionalGeneration.from_pretrained(
            'facebook/mbart-large-50-many-to-many-mmt'
        ).to(self.device)
        self.tokenizer = MBart50TokenizerFast.from_pretrained('facebook/mbart-large-50-many-to-many-mmt')
        self.tokenizer.src_lang = 'ru_RU'

    def translate(self, text, src_lang='en_XX'):
        '''
        Translates the given text to the specified source language.

        Args:
            text (str): The input text to be translated.
            src_lang (str): The source language code (default is 'en_XX' for English).

        Returns:
            list: A list containing the translated text.
        '''
        encoded_text = self.tokenizer(text, return_tensors='pt').to(self.device)

        generated_tokens = self.model.generate(
            **encoded_text,
            forced_bos_token_id=self.tokenizer.lang_code_to_id[src_lang]
        )

        res = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

        return res