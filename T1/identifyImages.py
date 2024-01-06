# TODO: Tudo o que não consegui fazer com Torch (T<num>) ou Numpy (N<num>) e outras partes (O<num>)
# N1 - Encontrar uma forma de usar o converters do loadtxt para converter string para numérico
# T1 - Adicionar coluna booleana chamada de OriginalImage com torch.Tensor.scatter_


from ProjetoRedesNeurais.auxiliary_func.getTimer import timer_data

import numpy as np
import torch
import csv
import os

from getFormatedExifData import generateExifDataset, getSpecificIndexes
from getFormatedExifData import base_path, data_path, csv_path, csv_filename1, filenames

from printListData import printListDataContent


def importCSVData():
    csv_data_numpy = np.loadtxt(
        csv_path+'/'+csv_filename1,
        dtype=np.float32,
        delimiter=';',
        skiprows=1
        # converters={i+1: lambda content: getConverters(content, i) for i in str_data_indexes[counter]}
    )
    return torch.from_numpy(csv_data_numpy)  # Returns a PyTorch Tensor


def main():
    # Generate csv file from exif data/raw data. it still needs to be changed later
    generateExifDataset()

    # Import csv data to a pytorch tensor
    exif_data = importCSVData()
    print(exif_data.shape)

    data = exif_data[:, :-1]  # all except the last column of each row
    target = exif_data[:, -1]  # only the last column of each row

    # Before the permutation of the columns, we need to reshape the tensor
    # Check if the tensor is contiguous and turning it contiguous if it's not
    isContiguous = exif_data.is_contiguous()
    if not isContiguous:
        exif_data = exif_data.contiguous()

    # Reshape tensor

    # Permute the tensor columns


    return


if __name__ == '__main__':
    timer_data(main)
