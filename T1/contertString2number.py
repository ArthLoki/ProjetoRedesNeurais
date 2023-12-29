import numpy as np
from datetime import datetime


def date2num(date):
    date_num = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    return int(date_num.timestamp())


def div_data2num(data):
    lDivData = data.split('/')
    print(data)

    if 's' in lDivData[1]:
        lDivData[1] = lDivData[1].split(' ')
        divData = float(lDivData[0])/float(lDivData[1][0])
    else:
        divData = float(lDivData[0])/float(lDivData[1])
    return divData


def offset_time2num(data):
    # Split the offset string into hours and minutes
    hours, minutes = map(int, data.split(':'))

    # Calculate the total offset in seconds
    total_seconds = hours * 3600 + minutes * 60

    return total_seconds


def str2num(data):
    hashed_value = hash(data)
    normalized_value = (hashed_value % 1000 + 1000) % 1000  # Garantir que esteja entre 0 e 1000
    return normalized_value


def convertDinamicallyData(data, str_data_indexes, dateIndexes, offsetTimeIndexes, divDataIndexes):

    content = list(data)
    for i in str_data_indexes:
        if i in dateIndexes:
            print(f'{i} - Date: {content[i]}')
            content[i] = date2num(content[i])
        elif i in offsetTimeIndexes:
            print(f'{i} - Offset: {content[i]}')
            content[i] = offset_time2num(content[i])
        elif i in divDataIndexes:
            print(f'{i} - DivData: {content[i]}')
            content[i] = div_data2num(content[i])
        else:
            print(f'{i} - Text: {content[i]}')
            content[i] = str2num(content[i])
        # print(f'{i} - {content[i]}')
    return content
