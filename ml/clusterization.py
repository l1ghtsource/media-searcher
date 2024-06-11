import pandas as pd
import numpy as np
import hdbscan
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import clickhouse_connect

# at this moment there were ~35,000 videos, the clusters were designed specifically for this number of videos

client = clickhouse_connect.get_client(host='91.224.86.248', port=8123)
TABLENAME = 'embeddings'

df = pd.read_csv(r'data\yappy_hackaton_2024_400k.csv')

new_df = client.query_df(f'SELECT id, clip_emb, ocr_emb, whisper_emb, whisper_len, ocr_len FROM {TABLENAME}')
new_df = new_df.drop_duplicates(subset='id')

embeddings = np.vstack(new_df['clip_emb'].values)

scaler = StandardScaler()
embeddings_scaled = scaler.fit_transform(embeddings)

pca = PCA(n_components=50)
embeddings_reduced = pca.fit_transform(embeddings_scaled)

clusterer = hdbscan.HDBSCAN(min_cluster_size=10, core_dist_n_jobs=-1)
labels = clusterer.fit_predict(embeddings_reduced)

new_df['cluster'] = labels

cluster_dict = new_df.groupby('cluster')['id'].apply(list).to_dict()

for cluster, ids in cluster_dict.items():
    cluster_dict[cluster] = [df.iloc[id_].link for id_ in ids]

mapping = {
    2: 'Озвучка',
    3: 'Гитара',
    6: 'ОГЭ И ЕГЭ',
    7: 'Здоровье',
    8: 'Пародии',
    10: 'Математика',
    11: 'Математика',
    14: 'FIFA',
    15: 'Хоккей',
    16: 'Фигурное катание',
    19: 'Мотоциклы',
    20: 'Причёски',
    24: 'Карточные игры',
    26: 'Единоборства',
    27: 'Футбол',
    28: 'Баскетбол',
    30: 'Мотоциклы',
    31: 'Мотоциклы',
    32: 'Мотоциклы',
    35: 'Животные',
    45: 'Одежда',
    46: 'Мода',
    47: 'Аутфиты',
    48: 'Клавиатуры',
    50: 'Тренировки',
    51: 'Здоровье',
    52: 'Фитнес',
    53: 'Красоты городов',
    54: 'Сноубординг',
    55: 'Футбол',
    57: 'Мультфильмы',
    58: 'Единоборства',
    59: 'Природа',
    60: 'Горы',
    61: 'Майнкрафт',
    62: 'Сёрфинг',
    63: 'Море',
    64: 'Рецепты',
    65: 'DIY & Art',
    68: 'Уход за собой',
    69: 'Dota 2',
    70: 'Маникюр',
    71: 'Макияж',
    72: 'Brawl Stars',
    73: 'Игровые приставки и ПК',
    74: 'Смартфоны и гаджеты',
    77: 'Смешарики',
    80: 'Кинематограф',
    83: 'Автомобили',
    86: 'Истории о мультфильмах',
    90: 'Интересные факты',
    91: 'Фрагменты из фильмов',
    92: 'Аниме',
    93: 'Genshin Impact',
    94: 'Мультфильмы',
    97: 'Исторические факты',
    98: 'Фрагменты из фильмов',
}

to_drop = [-1, 0, 1, 4, 5, 9, 12, 13, 17, 18, 21, 22, 23, 25, 29, 33, 34, 36, 37, 38, 39,
           40, 41, 42, 43, 44, 49, 56, 66, 67, 75, 76, 78, 79, 81, 82, 84, 85, 87, 88, 89, 95, 96]

df_clusters = pd.DataFrame(new_df.groupby('cluster')['id'].apply(list))

df_clusters['links'] = df_clusters['id'].apply(lambda ids: [df.iloc[id_].link for id_ in ids])  # get links by ID
df_clusters = df_clusters.reset_index()

df_clusters = df_clusters[~df_clusters['cluster'].isin(to_drop)]  # drop small and strange clusters
df_clusters['name'] = [mapping[id_] for id_ in df_clusters.cluster]  # give the clusters names


def combine_lists(x):
    combined = []
    for sublist in x:
        combined.extend(sublist)
    return list(set(combined))


agg_func = {
    'cluster': 'first',
    'id': combine_lists,
    'links': combine_lists
}


# repeating names will be combined into identical clusters
df_clusters_new = df_clusters.groupby('name').agg(agg_func).reset_index()

df_clusters_new.to_csv(r'data\final_clusters.csv')
