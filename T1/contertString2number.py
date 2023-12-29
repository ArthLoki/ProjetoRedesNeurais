import numpy as np
from datetime import datetime


def date2num(date):  # index from dateIndexes
    date_num = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    return int(date_num.timestamp())


def str2num(data):
    hashed_value = hash(data)
    normalized_value = (hashed_value % 1000 + 1000) % 1000  # Garantir que esteja entre 0 e 1000
    return normalized_value
