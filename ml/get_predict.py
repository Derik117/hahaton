import os
import pickle
from typing import Dict, List
import pandas as pd
from data import models
from scipy.sparse import csc_matrix
from sklearn.metrics.pairwise import cosine_distances
import numpy as np

from hahaton.settings import BASE_DIR

ratings = None
m = None


def load_ratings():
    global ratings, m
    if os.getenv('TEST'):
        limit = 100000
    else:
        limit = 999999999
    if ratings is None:
        print('loading')
        ratings = pd.DataFrame(models.MlRating.objects.values_list(named=True)[:limit])
        m = csc_matrix(([1] * len(ratings), (ratings['reader_id'].astype(int).values,
                                             ratings['doc_id'].astype(int).values)))
        print('loading complete')


load_ratings()


def get_predicts(user_id: int) -> Dict[str, List[int]]:
    '''
    :param user_id : id from "data.User"
    :return: {'books': [book_1_id, book_2_id, ...],
              'events': [event_1_id, event_2_id, ...],
              'services': [service_1_id, service_2_id, service_3_id, ...]
             }
    '''
    books = get_top_books(user_id)
    events = []
    services = []
    return {
        'books': books,
        'events': events,
        'services': services,
    }


def get_top_books(reader_id, n_books=30):
    global m
    if m is None:
        load_ratings()
    dist = (1 - cosine_distances(m, m[reader_id])).reshape(-1, )
    w = np.array(list(zip(sorted(dist), np.argsort(dist)))[::-1][:100])[1:, 0]
    i = np.array(list(zip(sorted(dist), np.argsort(dist)))[::-1][:100])[1:, 1]
    m2 = m[i].toarray()
    return np.argsort((m2.T * w).T.sum(axis=0))[::-1][:n_books]


def get_top_events(user_id: int):
    return [31776,
            31782,
            31820,
            31868,
            31870,
            31874,
            31880,
            31882,
            31897,
            31911,
            31958,
            31965,
            31966,
            31967,
            31968,
            32004,
            32010,
            32019,
            32029,
            32030,
            32033,
            32038,
            32040,
            32043,
            ]


service_df = pd.read_csv(os.path.join(BASE_DIR, 'ml', 'service_df.csv'))
df_pupil = pd.DataFrame(models.ServiceUser.objects.values_list(named=True)).rename(columns={'id': 'id_ученика',
                                                                                            'age': 'возраст'})
with open(os.path.join(BASE_DIR, 'ml', 'cosine_sim'), 'rb') as f:
    M_service = pickle.load(f)


def get_top_services(age: int, n: int = 20):
    class_ids = []
    if age > 90:
        age = 90
    elif age < 0:
        age = 0
    new_user_id = df_pupil.loc[(df_pupil['возраст'] == age), ['id_ученика']].values.reshape(-1, )[0]
    dist = cosine_distances(M_service, M_service[new_user_id]).reshape(-1, )
    for classif in dist.argsort()[-200:][::-1]:
        try:
            class_ids.append(service_df.loc[service_df['id_ученика'] == classif, 'Классификатор_услуги'].values[0])
        except:
            continue
    seen = set()
    seen.add(3003269)
    seen.add(3220710)
    uniq = []
    for x in class_ids:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    services = models.Service.objects.filter(created_at__gt='2020-01-01',
                                             service_class_id__in=uniq).order_by('-created_at').values_list('id',
                                                                                                            flat=True)
    return services[:n]
