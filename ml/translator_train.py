import random
import pickle
from transformers import MarianMTModel, MarianTokenizer, Trainer, TrainingArguments
from datasets import Dataset

# u can find trained model at https://huggingface.co/lightsource/yappy-fine-tuned-opus-mt-ru-en

path = r'data\translations.txt'

data = {'translation': []}

with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        ru, en = line.strip().split('\t')
        data['translation'].append({'ru': ru,  'en': en})

# add some more words for the littlest Yappy lovers
with open(r'data\zoomer_words.pkl', 'rb') as f:
    new = pickle.load(f)

d_train = data['translation'][:8000]
for _ in range(5):
    d_train.extend(new)

d_eval = data['translation'][8000:]
for _ in range(2):
    d_eval.extend(new)

random.shuffle(d_train)
random.shuffle(d_eval)

data_train = {'translation': d_train}
data_eval = {'translation': d_eval}

train_dataset = Dataset.from_dict(data_train)
eval_dataset = Dataset.from_dict(data_eval)

model_name = 'Helsinki-NLP/opus-mt-ru-en'

tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)


def preprocess_function(examples):
    inputs = [ex['ru'] for ex in examples['translation']]
    targets = [ex['en'] for ex in examples['translation']]
    model_inputs = tokenizer(inputs,
                             text_target=targets,
                             truncation=True,
                             padding='max_length',
                             max_length=128)
    return model_inputs


tokenized_dataset_train = train_dataset.map(preprocess_function, batched=True)
tokenized_dataset_eval = eval_dataset.map(preprocess_function, batched=True)

training_args = TrainingArguments(
    output_dir='./results',
    eval_strategy='epoch',
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset_train,
    eval_dataset=tokenized_dataset_eval,
)

trainer.train()

model.save_pretrained(r'data/fine-tuned-opus-mt-ru-en')
tokenizer.save_pretrained(r'data/fine-tuned-opus-mt-ru-en')
