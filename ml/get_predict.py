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


def get_top_books(reader_id, n_books=100):
    global ratings, m
    if ratings is None:
        print('loading')
        ratings = pd.DataFrame(models.MlRating.objects.values_list(named=True))
        m = csc_matrix(([1] * len(ratings), (ratings['reader_id'].astype(int).values,
                                             ratings['doc_id'].astype(int).values)))
        print('loading complete')
    dist = (1 - cosine_distances(m, m[reader_id])).reshape(-1, )
    w = np.array(list(zip(sorted(dist), np.argsort(dist)))[::-1][:100])[1:, 0]
    i = np.array(list(zip(sorted(dist), np.argsort(dist)))[::-1][:100])[1:, 1]
    m2 = m[i].toarray()
    return np.argsort((m2.T * w).T.sum(axis=0))[::-1][:n_books]
