import pandas as pd
import numpy as np
import hdbscan
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import clickhouse_connect

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
    # 0: 'Раскраски',
    # 1: 'Узбекистан',
    2: 'Озвучка',  # ЧЕЛОВЕК норм кластер
    3: 'Гитара',  # крутой кластер
    # 4: 'Странные анимации',
    # 5: 'Автомобили', # ЧЕЛОВЕК
    6: 'ОГЭ И ЕГЭ',  # крутой кластер
    7: 'Здоровье',  # норм кластер
    8: 'Пародии',  # огромный кластер со странным контентом
    # 9: 'ТЦ Пранки?', # ЧЕЛОВЕК
    10: 'Математика',  # ЧЕЛОВЕК крутой кластер
    11: 'Математика',  # 2 человека крутой кластер
    # 12: 'Музыка 80-х и 90-х', # норм кластер
    # 13: 'Сгенерировала нейросеть', # норм кластер
    14: 'FIFA',  # норм кластер
    15: 'Хоккей',  # крутой кластер
    16: 'Фигурное катание',  # крутой кластер
    # 17: 'Перемешались 2 чела и дота', # дропнуть
    # 18: 'Геймдев', # ЧЕЛОВЕК
    19: 'Мотоциклы',  # норм кластер
    20: 'Причёски',  # крутой кластер
    # 21: 'Таро', # до связи...
    # 22: 'Дикая природа', # дроп?
    # 23: 'Снежная королева', # дроп?
    24: 'Карточные игры',  # норм кластер
    # 25: 'Всратые скетчи', # ЧЕЛОВЕК
    26: 'Единоборства',  # норм кластер
    27: 'Футбол',  # крутой кластер
    28: 'Баскетбол',  # крутой кластер
    # 29: 'Гадалка со странными видео', # ЧЕЛОВЕК
    30: 'Мотоциклы',  # норм кластер, объединить с 19 тут в лесу и еще в странных местах
    31: 'Мотоциклы',  # норм кластер, объединить с 19 тут в городе
    32: 'Мотоциклы',  # норм кластер, объединить с 19 тут скорее гонки
    # 33: 'Бля))', # дроп
    # 34: 'Массаж', # хз наверное дроп
    35: 'Животные',  # норм кластер точно оставить
    # 36: 'Прыжки с парашюта', # хз мб норм
    # 37: 'Ааа женщина', # дроп
    # 38: 'Бубс', # дроп
    # 39: 'Почти бубс', # дроп
    # 40: 'Японские девочки...',
    # 41: 'Опять бубс', # дроп
    # 42: 'Видео про футбол', # ЧЕЛОВЕК
    # 43: 'Мужик в трусах', # дроп
    # 44: 'Небоскребы', # хз вроде и норм но зачем
    45: 'Одежда',
    46: 'Мода',
    47: 'Аутфиты',  # ОГРОМНЫЙ кластер надо оставить
    48: 'Клавиатуры',  # кайф кластер оставляем
    # 49: 'Растяжка', # дроп
    50: 'Тренировки',  # нуу норм
    51: 'Здоровье',  # ЧЕЛОВЕК
    52: 'Фитнес',  # ну это еще норм
    53: 'Красоты городов',  # нормик
    54: 'Сноубординг',  # крутой кластер
    55: 'Футбол',  # склеить с 27
    # 56: 'Какой-то мульт я хз', # дроп
    57: 'Мультфильмы',  # норм кластер
    58: 'Единоборства',  # склеить с 26
    59: 'Природа',  # крутой кластер
    60: 'Горы',  # норм кластер мб склеить с 59
    61: 'Майнкрафт',  # нуу вроде норм
    62: 'Сёрфинг',  # норм кластер
    63: 'Море',  # крутой кластер
    64: 'Рецепты',  # хороший кластер
    65: 'DIY & Art',  # странный кластер
    # 66: 'Странная игра', # дроп
    # 67: 'GTA', # ЧЕЛОВЕК +немного мусора
    68: 'Уход за собой',  # мб норм
    69: 'Dota 2',  # кайф кластер
    70: 'Маникюр',  # мб норм
    71: 'Макияж',  # ОГРОМНЫЙ кластер оставляем
    72: 'Brawl Stars',  # я его нашел
    73: 'Игровые приставки и ПК',  # нормик
    74: 'Смартфоны и гаджеты',  # большой кластер норм
    # 75: 'Чел залил миллион однотипных видосов в подписями', # ЧЕЛОВЕК
    # 76: 'Коллекционные автомобили', # норм но хз зачем
    77: 'Смешарики',  # кайф кластер
    # 78: 'Опять скетчи', # ЧЕЛОВЕК
    # 79: 'Всякие истории', # ЧЕЛОВЕК
    80: 'Кинематограф',  # ЧЕЛОВЕК норм кластер
    # 81: 'Counter-Strike', # ЧЕЛОВЕК
    # 82: 'Игры в которые играет твой батя', # хз странно
    83: 'Автомобили',  # большой кластер пойдет
    # 84: 'Зиро коментс', # хд
    # 85: 'Намешано все', # дроп
    86: 'Истории о мультфильмах',  # ЧЕЛОВЕК +- норм
    # 87: 'Новости Казахстана', # втф...
    # 88: 'Алкоголизм', # ЧЕЛОВЕК мужик ты куда
    # 89: 'Отношения', # ЧЕЛОВЕК хз дроп думаю
    90: 'Интересные факты',  # реально норм вроде
    91: 'Фрагменты из фильмов',  # хз +- норм
    92: 'Аниме',  # ОГРОМНЫЙ кластер оставляем
    93: 'Genshin Impact',  # ну почему бы и нет))
    94: 'Мультфильмы',  # приклеить к 57
    # 95: 'Смешались рассказы про аниме и геншин', # тут мало можно дропать
    # 96: 'Опять таро..', # дроп
    97: 'Исторические факты',  # хороший кластер
    98: 'Фрагменты из фильмов',  # склеить с 91
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