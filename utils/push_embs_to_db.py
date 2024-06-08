import clickhouse_connect
import tqdm
import os
from urllib.request import urlopen
from shutil import copyfileobj

from ml.meta_model import MetaModel


client = clickhouse_connect.get_client(host='91.224.86.248', port=8123)
TABLENAME = 'embeddings'


meta = MetaModel()


def load_from_csv(path, start, count):
    '''
    Loads video data from a CSV file.

    Args:
        path (str): The path to the CSV file.
        start (int): The starting index for loading data.
        count (int): The number of records to load.

    Returns:
        list: A list of lists, each containing the video ID, URL, and text description.
    '''
    with open(path, encoding='utf-8') as f:
        text = f.read().split('\nhttps://cdn-st.rutubelist.ru')
    try:
        text = text[start + 1:start + count + 1]
    except IndexError:
        text = text[start + 1:]
    videos = list(map(lambda x: [start + x[0]] + x[1].split(','), enumerate(text)))
    return [[i[0], 'https://cdn-st.rutubelist.ru' + i[1], ','.join(i[2:])] for i in videos]


def download_to(url, path):
    '''
    Downloads a file from a URL to a specified path.

    Args:
        url (str): The URL to download the file from.
        path (str): The path to save the downloaded file.
    '''
    with urlopen(url) as in_stream, open(str(path), 'wb') as out_file:
        copyfileobj(in_stream, out_file)


def iteration(fp, count, max_id=-1):
    '''
    Processes a batch of video files, extracts embeddings, and inserts them into a ClickHouse database.

    Args:
        fp (str): The file path to the CSV file containing video metadata.
        count (int): The number of video records to process.
        max_id (int, optional): The maximum ID to start processing from. Defaults to -1.
    '''
    if max_id == -1:
        max_id = client.query(f'SELECT max(id) FROM {TABLENAME}').result_columns
        print('maxid', max_id)
        max_id = max_id[0][0] + 1
    videos = load_from_csv(fp, max_id, count)
    data = []
    for video in tqdm.tqdm(videos):
        fname = str(video[0]) + '.mp4'
        url = video[1]
        download_to(url, fname)
        print(fname)
        embs = meta.get_embeddings(fname)
        data.append([video[0]] + list(embs))
        os.remove(fname)

    client.insert(TABLENAME, data, column_names=['id', 'clip_emb', 'ocr_emb', 'whisper_emb', 'whisper_len', 'ocr_len'])


# start_id = <your start id>
# for i in range(<num of iterations>):
#     iteration(r'data\yappy_hackaton_2024_400k.csv', 10, start_id + (i * 10))
