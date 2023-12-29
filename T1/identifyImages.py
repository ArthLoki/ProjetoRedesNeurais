# from ProjetoRedesNeurais.auxiliary_func.getPath import get_base_path
from ProjetoRedesNeurais.auxiliary_func.getTimer import timer_data

import numpy as np
import torch
import csv
import os

from getFormatedExifData import generateExifDataset, getSpecificIndexes
# from getFormatedExifData import getSpecificIndexesFromContent, getMultSpecificIndexesFromContent
from getFormatedExifData import base_path, data_path, csv_path, csv_filename, filenames

from contertString2number import str2num, date2num

from printListData import printListDataContent


global str_data_indexes, dateIndexes, all_content
str_data_indexes = []
dateIndexes = []
all_content = []


def importCSVData(counter):
    csv_data_numpy = np.loadtxt(
        csv_path+'/'+csv_filename,
        dtype=np.float32,
        delimiter=';',
        skiprows=1,
        converters={i: lambda content: getConverters(content, i) for i in str_data_indexes[counter]}
    )
    return torch.from_numpy(csv_data_numpy)  # Returns a PyTorch Tensor


# def getConverters(content):
#     converters = {}
#
#     # add texts
#     for i in str_data_indexes:
#         converters[i] = str2num(content, i)
#
#     # add date
#     for j in dateIndexes:
#         converters[j] = date2num(content, j)
#
#     return converters

def getConverters(content, i):
    print(dateIndexes[i])

    content = list(content)
    if i in list(dateIndexes[i]):
        return date2num(content[i])
    else:
        return str2num(content[i])


# REFORMULAR
# def getOgColumnList():
#     ogColumnList = []
#
#     # 1 - get image filenames, creating a list
#     imageIdentifierColumnList = getImageIdentifierColumnList()
#
#     # 2 - check if 'og' is in each filename in this list. If so, append 1.0 to the ogColumnList, else append 0.0
#     for name in imageIdentifierColumnList:
#         if 'og' in name:
#             ogColumnList.append(1.0)
#         else:
#             ogColumnList.append(0.0)
#
#     # 3 - return ogColumnList
#     return ogColumnList


def main():
    global str_data_indexes, dateIndexes, all_content

    counter = 0

    # generate csv file from exif data/raw data. it still need to be changed later
    data = generateExifDataset()

    all_content = data[0]
    dateIndexes = data[1]
    str_data_indexes = data[2]

    # printListDataContent(all_content)
    # print('\n')
    # printListDataContent(dateIndexes)
    # print('\n')
    # printListDataContent(str_data_indexes)

    # import csv data to a pytorch tensor
    exif_data = importCSVData(counter)
    print(exif_data.shape)

    counter += 1
    return


if __name__ == '__main__':
    timer_data(main)
