# Лидеры Цифровой Трансформации 2024

*MISIS ITUT ITAM team*

Team Members:
1) **Егор Чистов** - Backend
2) **Дмитрий Коноплянников** - Frontend
3) **Анна Гулякина** - Design
4) **Кирилл Рыжичкин** - ML Engineer
5) **Артём Плужников** - ML Engineer

Презентация: [тык](https://disk.yandex.ru/i/YWLpgGftE838KA)

Веб-сервис: [тык](https://itut.itatmisis.ru/)

Swagger API docs: [тык](https://itut.itatmisis.ru/api/docs)

## Кейс "Сервис текстового поиска по медиаконтенту" (Yappy)

> В библиотеке Yappy десятки миллионов коротких видео. Возможность быстро и эффективно находить интересующий контент улучшает пользовательский опыт, помогает найти новые интересы пользователя и улучшить рекомендации. Разработайте сервис, позволяющий индексировать и осуществлять поиск по видео на основе медиаконтента. Сервис должен уметь обрабатывать запросы пользователей, извлекать из них ключевые слова и на их основе осуществлять поиск релевантных видеофайлов.

## Предложенное решение

### Для извлечения фичей из видео использовались следующие подходы:
1) __CLIP__ (а именно *Searchium-ai/clip4clip-webvid150k*, обученный на парах "поисковый запрос - видео") - строим эмбеддинги видео (пространство этих эмбеддингов устроено так, что в нём векторные представления близких текстов и видео тоже близки, то есть эмбеддинги слова "кот" и видео с котом будут иметь высокие показатели близости, а это именно то, что нам и надо)
![scheme_clip](clip_scheme.png)
3) __OCR + Text Embedding__ - извлекаем текст из видео с помощью *EasyOCR* (берём фреймы каждые 3 секунды, далее считываем с них текст, чтение текста по фреймам распараллелено, это позволило значительно повысить скорость обработки одного видео), далее строим эмбеддинг текста с помощью *all-MiniLM-L6-v2*.
Это позволяет работать с видео, характерными для формата Yappy и Tiktok - когда на фоне просто нарезка каких-то фрагментов из игр или фильмов, а основная информация содержится в тексте, наложенном на видео.
![scheme_ocr](easyocr_scheme.jpeg)
5) __VAD + ASR + Text Embedding__ - используем *silero-vad* для нахождения фрагментов аудиодорожки видео с голосом, транскрибируем с помощью *whisper-medium*, далее строим эмбеддинг текста с помощью *all-MiniLM-L6-v2*.
Это позволяет работать с видео, в которых основная информация содержится в их аудиосоставляющей. Более того, в том случае, когда в аудио вместо речи играет музыка, whisper возвращает "МУЗЫКА", а если аплодисменты, то "АПЛОДИСМЕНТЫ" и т.д, то есть данная модель устойчива к различным видам аудио.
![scheme_asr](whisper_scheme.png)

### Замеры скорости на видео длительностью 25 секунд:

<div align="center">
   
| Модель          | Время GPU (s) | Время CPU (s) |
|-----------------|-----------------|-----------------|
| [clip_model.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/clip_model.py)   | 4.3             | 7.5             |
| [whisper_model.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/whisper_model.py)| 2.68 (medium)   | 6 (base)        |
| [ocr_model.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/ocr_model.py)    | 2.23            | 21              |
| [meta_model.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/meta_model.py) (объединяет в себя все прошлые пункты)   | 8               | 32              |

Изначально *OCRModel* считывал текст с фреймов последовательно, а в *MetaModel* происходило распараллеливание *CLIPModel*, *OCRModel* и *WhisperModel*. Однако, когда мы начали проводить замеры скорости на CPU, было обнаружено, что если распараллелить именно процесс считывания текста с фреймов в *OCRModel*, то скорость значительно возрастет. То есть сначала на все возможные ресурсы параллелится *OCRModel*, а когда считываение текста завершится уже *CLIPModel* и *WhisperModel* распределяют ресурсы между собой. Это ускорило инференс на CPU с одной минуты до 20 секунд!

</div>

### Обработка поискового запроса:
1) __CLIP Embedding__ - строим с помощью *clip4clip-webvid150k* векторное представление поискового запроса для мэтчинга с CLIP-эмбеддингами видео
2) __Text Embedding__ - строим с помощью *all-MiniLM-L6-v2* векторное представление поискового запроса для мэтчинга с эмбеддингами видео (векторными представлениями текстов, полученных с OCR и ASR)
3) __Ranking__ - на основании полученных эмбеддингов переведенного поискового запроса и эмбеддингов видео, содержащихся в БД *Clickhouse*, проводим быстрый поиск top-k похожих видео с помощью *faiss*, также здесь автоматически рассчитываются веса OCR, ASR и CLIP, на основании количества слов, распознанных *Whisper* и *EasyOCR*

### Замеры скорости:

<div align="center">
   
| Модель          | Время GPU (ms) | Время CPU (ms) |
|-----------------|-----------------|-----------------|
| [text2clip_model.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/text2clip_model.py) (построение эмбеддинга)| 17           | 50             |
| [text2minilm_model.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/text2minilm_model.py) (построение эмбеддинга)| 8   | 22        |
| [ranker.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/ranker.py)<br>(включая перевод, построение эмбеддингов и сам поиск top-k при k=20)| 211               | 323              |

</div>

## Кластеризация или поиск видео по тематикам

Имея значительное количество строк в БД с эмбеддингами видео, захотелось провести их кластеризацию. К эмбеддингам *CLIP* были применены стандартизация, *PCA* с 50 главными компонентами, затем был использован алгоритм *hdbscan* непосредственно для кластеризации. Было получено 98 различных кластеров, содержащих внутри себя видео одной тематики, дальше кластерам были даны названия и была проведена их фильтрация. В итоге осталось 48 качественных кластеров. Таким образом, у пользователя помимо опции обычного поиска подходящих видео по его запросу появилась опция выбрать определенный кластер, внутри которого содержатся точно отобранные видео на одну определённую тематику, соответствующую названию кластера.

Для удобного добавления видео были рассчитаны средние эмбеддинги для каждого кластера, при загрузке видео мы добавляем его в наиболее подходящий кластер, основываясь на значении косинусной близости CLIP-эмбеддинга загруженного видео со средним CLIP-эмбеддингом всего кластера.

Код кластеризации: [clusterization.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/clusterization_by_themes.py)

Полученные кластеры: [final_clusters.csv](https://github.com/l1ghtsource/media-searcher/blob/main/data/final_clusters.csv)

## Fine-tuning переводчика на собственном датасете

Перед нами встала проблема: использовать API Google Translator и других популярных переводчиков запрещено, а open-source решения, к удивлению, не справляются с простыми запросами. Например, на запрос "роблокс", все популярные модели с huggingface выдавали результат "robls" или "roblocks", а эмбеддинг этого слова в CLIP-пространстве был далек от непосредственно роблокса и близок к блокам, что портило поисковую выдачу. На запрос "райан гослинг" маленькими буквами модель вовсе давала ответ "I'll take care of you. I'll take care of you". Поэтому, из популярных под видео тэгов Yappy, а также некоторых добавленных слов был [собран](https://github.com/l1ghtsource/media-searcher/blob/main/utils/generate_dataset_for_translator_tuning.py) небольшой датасет из 10000 русских слов, далее эти слова были переведены с помощью Google Translator на английский и на полученных парах слов была [дообучена](https://github.com/l1ghtsource/media-searcher/blob/main/ml/translator_train.py) модель машинного перевода *Helsinki-NLP/opus-mt-en-ru*. Модель выбирали исходя из [бенчмарков](https://huggingface.co/spaces/utrobinmv/TREX_benchmark_en_ru_zh) по соотношению скорости и качества ru-en перевода.

Модель: https://huggingface.co/lightsource/yappy-fine-tuned-opus-mt-ru-en

Исходная модель для сравнения: https://huggingface.co/Helsinki-NLP/opus-mt-ru-en

## Автоисправление и автопродолжение запроса

Перед нами встала задача: реализовать атодополнение поискового запроса, то есть показывать юзеру при вводе поискового запроса n-кандидатов на заполнение поисковой строки. Так как контент в Yappy довольно специфичный, не предоставляется возможности спарсить список поисковых запросов и составить из него словарь, как это сделал Ozon и Lamoda, поэтому мы сгенерировали тестовый соварь языковой моделью. При разработки своего решения мы отчасти вдохновлялись результатами и архитектурой именно этих компаний. Изначально мы попробовали elasticsearch и manticore, но результаты этих open-source решений нас не удовлетворили как по скорости, так и по качеству предоставления n-кандидатов на заполнение поисковой строки. Мы пробовали предобучить ruRoBERTa и использовать эту модель для предсказания следующего слова, но результат нас опять не устроил. 

Методом проб и ошибок мы пришли к финальной архитектуре: сначала мы используем алгоритм на n-граммах, c помощью него мы получаем топ-5 кандидатов на заполнение поисковой строки, для повышения точности рекомендации мы переводим топ-5 кандидатов в векторное пространство через multilingual-e5-small и кластерезуем полученные эмбеддинги, самый большой кластер переходит на следующий этап: мы получаем из базы данных эмбеддинги 10 последних запросов юзера и сравниваем их косинусной близостью с кластером — тем самым получаем ранжированный список n-кандидатов по похожести на последние 10 запросов юзера.

## Кластеризация видео по действующим лицам

Также у нас появилась идея - кластеризовать видео по лицам, участвующих в них. Для этого использовали *opencv* и *face_recognition*, мы находим уникальные лица на видео и возвращаем эмбеддинг самого часто встречающегося лица. На обработку 1000 видео на CPU уходило примерно 3 часа, на GPU не завелось :(

Полученные 31000 эмбеддингов кластеризовали с *PCA* и *hdbscan*, получили 138 кластеров, из них отобрали 80 качественных.

Среднее время обработки одного видео:

<div align="center">

| Модель          | Время GPU (s) | Время CPU (s) |
|-----------------|-----------------|-----------------|
| [face_founder_model.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/face_founder_model.py) | -           | 10             |

</div>

Код кластеризации: [clusterization_by_faces.py](https://github.com/l1ghtsource/media-searcher/blob/main/ml/clusterization_by_faces.py)

Полученные кластеры: [faces-31000-videos-filtered.csv](https://github.com/l1ghtsource/media-searcher/blob/main/data/faces-31000-videos-filtered.csv)

## Kaggle ноутбуки

<div align="center">

| Ноутбук                                           | Описание                                     |
|---------------------------------------------------|----------------------------------------------|
| [Ноутбук с OCR, ASR, CLIP, Ranker, кластеризацией по тематикам и замерами скорости](https://www.kaggle.com/code/l1ghtsource/yappy-hackathon/) | Включает основные классы и замеры времени на GPU и CPU. |
| [Ноутбук с файн-тюнингом переводчика](https://www.kaggle.com/code/l1ghtsource/transaltor-finetune/) | Содержит файн-тюнинг переводчика на собственном датасете. |
| [Ноутбук с кластеризацией видео по лицам](https://www.kaggle.com/code/l1ghtsource/yappy-faces-clustering/) | Содержит код для кластеризации видео по лицам. |
| [Ноутбук с поиском средних векторов кластеров](https://www.kaggle.com/code/l1ghtsource/yappy-cluster-mean-embeddings/) | Содержит код для поиска средних векторов кластеров и поиск подходящего кластера для данного видео. |
| [Ноутбук с AutocompleteService](https://www.kaggle.com/code/l1ghtsource/yappy-autocomplete) | Содержит код системы автопродолжение и исправления поискового запроса. |

</div>

### Backend составляющая:

 - 1 контейнер под API
 - 7 контейнеров под ML модели
 - 2 бакета Object Storage (для хранения картинок лиц и видео)
 - clickhouse для хранения эмбеддингов
 - PostgreSQL для хранения информации о видео, кластерах лицах, и их связях 
 - traefik в режиме reverse-proxy 
 - kafka с zookeeper

### Схема:

<div align="center">
   
![back](back.png)

</div>

### Инструкции к запуску:

Сконфигурируйте .env файл:
```
CLICKHOUSE_HOST=<IP-адрес кликхауса>
CLICKHOUSE_USERNAME=<авторизация кликхауса>
CLICKHOUSE_PASSWORD=<авторизация кликхауса>

POSTGRES_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME - адрес постгрес
```

Адреса контейнеров с поиском, переводчиком и Text2MiniLM (планировалась возможность запускать на разных хостах для большей производительности)

```
TRANSLATOR_URL=http://translator 
TEXTEMBEDDER_URL=http://textembedder
SEARCH_URL=http://search

KAFKA_URL=kafka:9092
```

Ключи авторизации к бакету Object Storage, где хранятся видео 

```
S3_PUBLIC=<ключи от Object Storage>
S3_SECRET=<ключи от Object Storage>
```

Пути к папкам ML моделей, все кроме OCR при первом запуске контейнера скачается автоматически

Модели OCR craft_mlt_25k.pth и cyrillic_g2.pth можно скачать с https://www.jaided.ai/easyocr/modelhub/

```
OCR_MODELS
EMBEDDING_MODEL
TRANSLATOR_MODEL
WHISPER_MEDIUM
WHISPER_BASE
CLIP_MODEL
CLIP_TEXT_MODEL
```

Сконфгурируйте конфиг traefik внутри `docker-compose.yaml`, после этого можно запускать через `docker compose up`

## Преимущества решения:
1) Быстрый поиск подходящих видео с помощью *faiss* (~300ms на CPU, ~200ms на GPU для топ-20 видео)
2) Извлекаем максимум информации: текст с видео (*EasyOCR*, причем извлекаем текст с фреймов параллельно, что даёт сильный прирост в скорости), текстовое представление аудиосоставляющей (*Whisper*), учитываем происходящее на видео (CLIP)
3) Автоматическое взвешивание суммы близостей по всем трём эмбеддингам в зависимости от количества распознанных слов *Whisper* и *EasyOCR* (то есть если *Whisper*'ом слов будет распознано мало - веса сместится на *CLIP* и *OCR*, и наоборот)
4) Возможность сортировки видео по тематикам (кластеризация по CLIP-эмбеддингам)
5) Возможность сортировки видео по персоналиям (будут найдены видео с конкретным человеком)
6) Собственный переводчик, зафайнтюненный на корпусе из популярных в Yappy слов (верно интерпретируем слэнг-запросы)
7) Мультиязычность (решение не зависит ни от языка видео, ни от языка поискового запроса)
8) Быстрое автопродолжение поискового запроса и автокорреция орфографических ошибок
9) Скорость построения новых эмбеддингов и занесения их в *Clickhouse*-хранилище, на GPU за 5-15с будут получены транскрибация, текст с видео, построены три эмбеддинга и занесены в БД
10) Real-time голосовой ввод в поле поиска
11) Независимость от тегов и описания видео (работаем только с медиа-контентом)

## Нереализованные идеи

1. Поиск видео по тональности (весёлые, грустные, смешные и т.д.)
   - [kaggle ноутбук с наработками](https://www.kaggle.com/code/l1ghtsource/yappy-sentiment/)
   - сначала попытались построить CLIP-эмбеддинги слов "sad", 'funny" и пр., далее рассчитать косинусную близость CLIP-эмбеддинга каждого видео с получеными векторами слов, далее с помощью softmax получили "вероятности" принадлежности видео каждому из классов, однако качество данной классификации нас не устроило
   - также была идея провести sentiment analysis по ocr и whisper эмбеддингам, для этого нашли модель (https://huggingface.co/shhossain/all-MiniLM-L6-v2-sentiment-classifier), работающую ровно с тем типом эмбеддингов, который мы используем, однако классы, на которых училась эта модель не совсем нам подходили, поэтому тоже решили отказаться от этой идеи (времени собрать датасет и обучить свою подобную модель уже не оставалось)
