import os
import pickle
from typing import Dict, List
import pandas as pd
from data import models
from scipy.sparse import csc_matrix
from sklearn.metrics.pairwise import cosine_distances
import numpy as np
import datetime as dt
from hahaton.settings import BASE_DIR

ratings = None
m = None
id_to_book = None
reader_to_id = None

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


events = pd.DataFrame(
    models.Event.objects.filter(start_date__isnull=False).values_list('id', 'age_group_ceil', 'start_date', named=True))


def get_top_events(age: int, n=10):
    f_events = events[events.start_date > dt.date.today()]
    np.random.seed(age)
    if age < 12:
        res = np.random.choice(f_events[(f_events.age_group_ceil >= 0) & (f_events.age_group_ceil < 18)]['id'], n,
                               replace=False)
    elif age < 18:
        res = np.random.choice(f_events[(f_events.age_group_ceil >= 0) & (f_events.age_group_ceil < 40)]['id'], n,
                               replace=False)
    elif age < 50:
        res = np.random.choice(f_events[(f_events.age_group_ceil >= 18) & (f_events.age_group_ceil < 999)]['id'], n,
                               replace=False)
    else:
        res = np.random.choice(f_events[(f_events.age_group_ceil >= 55) & (f_events.age_group_ceil < 999)]['id'], n,
                               replace=False)
    return res


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
    dist_idx = dist.argsort()
    for classif in dist_idx:
        if len(np.unique(class_ids)) < n:
            try:
                class_ids.append(service_df.loc[service_df['id_ученика'] == classif, 'Классификатор_услуги'].values[0])
            except:
                continue
        else:
            break
    seen = set()
    seen.add(3003269)
    seen.add(3220710)
    uniq = []
    for x in class_ids:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    services = models.Service.objects.filter(created_at__gt='2016-01-01',
                                             service_class_id__in=uniq).order_by('-created_at').values_list('id',
                                                                                                            'service_class_id',
                                                                                                            'organization_id',
                                                                                                            'schedule_type',
                                                                                                            named=True).distinct()
    service_ids = pd.DataFrame(services).drop_duplicates(['service_class_id', 'organization_id',])[
        'id'].values
    return service_ids[:n]
