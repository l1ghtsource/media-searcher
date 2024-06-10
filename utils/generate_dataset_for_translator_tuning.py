import pandas as pd
import re
from tqdm import tqdm
from deep_translator import GoogleTranslator

df = pd.read_csv(r'data\yappy_hackaton_2024_400k.csv')
df = df.dropna().reset_index(drop=True)


# leave only Russian words (without emoji and English words)
def func(text): return re.sub(r'[^А-Яа-яЁё\s]+', '', text)


df['cleaned_description'] = df['description'].apply(func)

df = df.dropna().reset_index(drop=True)

russian_phrases = []

for i in range(len(df)):
    russian_phrases.extend([word.lower() for word in df.cleaned_description[i].split() if len(word) > 3])

russian_phrases = list(set(russian_phrases))[:10000]  # 10,000 is enough for us

# let's add requests for connoisseurs of high art ;)
russian_phrases.extend([
    'роблокс',
    'роблоксер',
    'бравл старс',
    'бравлстарс',
    'кейпоп',
    'кей поп',
    'майнкрафт',
    'скибиди туалет',
    'мэйби бэйби',
    'дота',
    'дота 2',
    'гача лайф',
    'таро'
])


translator = GoogleTranslator(source='ru', target='en')

translations = []

for phrase in tqdm(russian_phrases):
    translated = translator.translate(phrase)
    translations.append((phrase, translated))

with open(r'data\translations.txt', 'w', encoding='utf-8') as f:
    for ru, en in translations:
        f.write(f'{ru}\t{en}\n')
