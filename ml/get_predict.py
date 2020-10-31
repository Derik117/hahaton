from typing import Dict, List
import pandas as pd
from data import models
from scipy.sparse import csc_matrix
from sklearn.metrics.pairwise import cosine_distances
import numpy as np

ratings = None
m = None


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
    global ratings, m
    if ratings is None:
        print('loading')
        ratings = pd.DataFrame(models.MlRating.objects.values_list(named=True)[:100000])
        m = csc_matrix(([1] * len(ratings), (ratings['reader_id'].astype(int).values,
                                             ratings['doc_id'].astype(int).values)))
        print('loading complete')
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


def get_top_services(user_id: int):
    return [116143,
            760923,
            336649,
            594380,
            1035694,
            1042251,
            117337,
            117338,
            117542,
            227527,
            227531,
            227530,
            478627,
            601744,
            604520,
            1011179,
            1019105,
            114900,
            118053,
            175309,
            229429,
            230286,
            310361,
            394149,
            581794,
            581836,
            722637,
            933924,
            116621,
            117786,
            222969,
            227131,
            227244,
            227247,
            227296,
            232643,
            232807,
            356151,
            356868,
            524600, ]
