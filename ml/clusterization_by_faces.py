import hdbscan
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import clickhouse_connect
import pandas as pd

df = pd.read_csv(r'data\yappy_hackaton_2024_400k.csv')

client = clickhouse_connect.get_client(host='91.224.86.248',
                                       port=8123,
                                       username=...,
                                       password=...)

df_faces = client.query_df(f'SELECT * FROM faces_embeddings')

embeddings = np.array(df_faces['face_emb'].tolist())

scaler = StandardScaler()
embeddings_scaled = scaler.fit_transform(embeddings)

pca = PCA(n_components=50)
embeddings_reduced = pca.fit_transform(embeddings_scaled)

clusterer = hdbscan.HDBSCAN(min_cluster_size=10, core_dist_n_jobs=-1)

cluster_labels = clusterer.fit_predict(embeddings_reduced)
df_faces['cluster'] = cluster_labels

cluster_dict = df_faces.groupby('cluster')['id'].apply(list).to_dict()

for cluster, ids in cluster_dict.items():
    cluster_dict[cluster] = [df.iloc[id_].link for id_ in ids]

to_drop = [-1, 0, 1, 15, 17, 20, 25, 28, 32, 34, 35, 37, 38, 42, 48, 50, 53, 56, 59, 63, 65, 68, 70, 71, 75, 80, 82, 83, 86, 88, 90,
           91, 93, 94, 95, 96, 99, 100, 101, 102, 104, 107, 108, 112, 114, 115, 116, 118, 125, 126, 128, 129, 130, 131, 132, 133, 134, 135, 137]

mapping = {
    2: 'про фильмы',
    3: 'про игры',
    4: 'про телефоны',
    5: 'интересные факты',
    6: 'про уход за кожей',
    7: 'про историю Росиии и СССР',
    8: 'про бизнес',
    9: 'про здоровье',
    10: 'про корабли',
    11: 'про макияж',
    12: 'про нейросети',
    13: 'про арабский язык',
    14: 'про counter-strike',
    16: 'разнобой',
    18: 'про телефоны',
    19: 'про макияж',
    21: 'про алкоголь',
    22: 'интересные факты',
    23: 'про китайский язык',
    24: 'про мультфильмы',
    26: 'про спорт',
    27: 'про телефоны',
    29: 'про здоровье',
    30: 'про прически',
    31: 'про речь',
    33: 'про доту',
    36: 'про математику',
    39: 'про историю России',
    40: 'про рецепты',
    41: 'скетчи',
    43: 'про gta',
    44: 'про бизнес',
    45: 'про макияж',
    46: 'про озвучку',
    47: 'про одежду',
    49: 'про макияж',
    51: 'про факты о животных',
    52: 'про психологию',
    54: 'про одежду',
    55: 'интересные факты',
    57: 'про макияж',
    58: 'разнобой',
    60: 'про математику',
    61: 'про макияж',
    62: 'про макияж',
    64: 'про рецепты',
    66: 'про жизнь',
    67: 'про ЕГЭ по истории',
    69: 'про историю',
    72: 'про рецепты',
    73: 'интересные факты',
    74: 'про аниме',
    76: 'про телефоны',
    77: 'про телефоны',
    78: 'про сериалы',
    79: 'про автомобили',
    81: 'разнобой',
    84: 'про фильмы и актеров',
    85: 'про одежду',
    87: 'про математику',
    89: 'про макияж',
    92: 'про одежду',
    97: 'про аниме',
    98: 'про макияж',
    103: 'разнобой',
    105: 'про психологию',
    106: 'папич',
    109: 'про поэтов',
    110: 'про игры',
    111: 'про технику',
    113: 'про русский язык',
    117: 'про геймдев',
    119: 'про мотоциклы',
    120: 'про речь',
    121: 'про игры',
    122: 'про макияж',
    123: 'про русский язык',
    124: 'про футбол',
    127: 'про восточные страны',
    136: 'про рецепты'
}

df_clusters = pd.DataFrame(df_faces.groupby('cluster')['id'].apply(list))
df_clusters['links'] = df_clusters['id'].apply(lambda ids: [df.iloc[id_].link for id_ in ids])
df_clusters = df_clusters.reset_index()

df_clusters = df_clusters[~df_clusters['cluster'].isin(to_drop)]
df_clusters['name'] = [mapping[id_] for id_ in df_clusters.cluster]

df_clusters.to_csv(r'data\faces-31000-videos-filtered.csv')
