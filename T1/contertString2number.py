import numpy as np
from datetime import datetime


def date2num(content, index):  # index from dateIndexes
    date_num = datetime.strptime(content[index], '%d/%m/%Y %H:%M:%S')
    return int(date_num.timestamp())


def str2num(content, index):  # index from str_data_indexes
    hashed_value = hash(content[index])
    normalized_value = (hashed_value % 1000 + 1000) % 1000  # Garantir que esteja entre 0 e 1000
    return normalized_value
