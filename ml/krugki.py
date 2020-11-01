import pandas as pd
import numpy as np
import pickle
import requests, zipfile
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict
import itertools
from scipy.sparse import csc_matrix
from sklearn.metrics.pairwise import cosine_distances

df_classes = pd.read_csv('classes.csv')
df_pupil = pd.read_csv('pupil.csv')
df_services = pd.read_csv('services.csv')
df_relation = pd.read_csv('relation.csv')
df = pd.read_csv('df.csv')

def get_predicts_age(age: int, n: int) -> List[int]:
    class_ids = []
    with open('cosine_sim', 'rb') as f:
        M = pickle.load(f)
    new_user_id = df_pupil.loc[(df_pupil['возраст'] == age), ['id_ученика']].values.reshape(-1, )[0]
    dist = cosine_distances(M, M[new_user_id]).reshape(-1, )
    dist_idx = dist.argsort()
    for classif in dist_idx:
        if len(np.unique(class_ids)) < n:
            try:
                class_ids.append(df.loc[df['id_ученика'] == classif, 'Классификатор_услуги'].values[0])
            except:
                continue
        else:
            break
    seen = set()
    uniq = []
    for x in class_ids:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    return uniq

def get_predicts(user_id: int, n: int) -> List[int]:
    class_ids = []
    with open('cosine_sim', 'rb') as f:
        M = pickle.load(f)
    age = df_pupil.loc[df_pupil['id_ученика'] == user_id, 'возраст'].values[0]
    if user_id in df_relation['id_ученика'].values:
        dist = cosine_distances(M, M[user_id]).reshape(-1, )
    else:
        new_user_id = df_pupil.loc[(df_pupil['возраст'] == age), ['id_ученика']].values.reshape(-1, )[0]
        dist = cosine_distances(M, M[new_user_id]).reshape(-1, )
    dist_idx = dist.argsort()
    for classif in dist_idx:
        if len(np.unique(class_ids)) < n:
            try:
                class_ids.append(df.loc[df['id_ученика'] == classif, 'Классификатор_услуги'].values[0])
            except:
                continue
        else:
            break
    seen = set()
    uniq = []
    for x in class_ids:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    return uniq

def get_krugki(ids: List[int]) -> List[int]:
    kr = []
    df_services_ = df_services.copy()
    df_services_ = df_services_.loc[~df_services_.duplicated(['Классификатор_услуги', 'id_организации', 'Тип_расписания']), :]
    df_services_ = df_services_.sort_values('Дата_создания', ascending=False)
    for i in ids:
        kr.append(df_services_.loc[(df_services_['Дата_создания'] > '2016-01-01') & (df_services_['Классификатор_услуги'] == i), 'id_услуги'].values.reshape(-1, )[0])
    return kr