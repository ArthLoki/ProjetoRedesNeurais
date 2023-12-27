from ProjetoRedesNeurais.auxiliary_func.getPath import get_base_path
from ProjetoRedesNeurais.auxiliary_func.getTimer import timer_data
import numpy as np
import torch
import csv
import os

from getFormatedExifData import generateExifDataset, getSpecificIndexes, getMultSpecificIndexes
from getFormatedExifData import base_path, data_path, csv_path, csv_filename, filenames


def importCSVData():
    csv_data_numpy = np.loadtxt(
        csv_path+'/'+csv_filename,
        dtype=np.float32,
        delimiter=';',
        skiprows=1
    )
    return torch.from_numpy(csv_data_numpy)  # Returns a PyTorch Tensor

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
    # generate csv file from exif data/raw data. it still need to be changed later
    generateExifDataset()

    # import csv data to a pytorch tensor
    # exif_data = importCSVData()
    # print(exif_data.shape)


if __name__ == '__main__':
    timer_data(main)

