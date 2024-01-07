# TODO: Tudo o que não consegui fazer com Torch (T<num>) ou Numpy (N<num>) e outras partes (O<num>)
# N1 - Usar o converters do loadtxt para converter string para numérico
# T1 - Adicionar coluna booleana chamada de OriginalImage usando torch.Tensor.scatter_


from ProjetoRedesNeurais.auxiliary_func.getTimer import timer_data

import numpy as np
import torch
import os

from getFormatedExifData import generateExifDataset, getSpecificIndexes, getHeaderList
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


def checkImageData(exif_data_permuted):
    data = exif_data_permuted[:, :-1]  # all except the last column of each row
    target = exif_data_permuted[:, -1]  # only the last column of each row

    col_list = getHeaderList()

    og_data = data[target == 1.0]
    not_og_data = data[target != 1.0]

    og_mean = torch.mean(og_data, dim=0)
    not_og_mean = torch.mean(not_og_data, dim=0)

    for i, args in enumerate(zip(col_list, og_mean, not_og_mean)):
        diff = abs(args[2].tolist() - args[1].tolist())
        print('{:2} - {:20}\t\t{:6.2f}\t\t{:6.2f}\t\t{:6.2f}'.format(i, *args, diff))

    # The original images seems to have a higher /Exif/Image/YResolution (7), /Exif/Photo/FocalLength (28),
    # /Exif/Photo/ColorSpace (29)
    # Meanwhile, the called 'not original images' seems to have higher /Exif/Photo/MaxAperture (25),
    # /Exif/Photo/MeteringMode (26)

    # Finding original images
    og_img_threshold = 468.40  # using /Exif/Image/YResolution (7)
    og_img_data = data[:, 7]
    og_predicted_indexes = torch.lt(og_img_data, og_img_threshold)

    # Finding 'not original' images
    not_og_img_threshold = 2088.43  # using /Exif/Photo/MaxAperture (25)
    not_og_img_data = data[:, 25]
    not_predicted_indexes = torch.lt(not_og_img_data, not_og_img_threshold)

    # the indexes of the actually original images
    og_actual_indexes = target == 1.0
    not_og_actual_indexes = target != 1.0
    print(og_actual_indexes.sum())
    print(not_og_actual_indexes.sum())

    # Comparing actual original images
    print('\n---> Original Images')
    n_matches_og = torch.sum(og_actual_indexes & og_predicted_indexes).item()
    n_predicted_og = torch.sum(og_predicted_indexes).item()
    n_actual_og = torch.sum(og_actual_indexes).item()
    print(n_matches_og, n_matches_og / n_predicted_og, n_matches_og / n_actual_og)

    # Comparing not original images
    print('\n---> Not Original Images')
    n_matches_nog = torch.sum(not_og_actual_indexes & not_predicted_indexes).item()
    n_predicted_nog = torch.sum(not_predicted_indexes).item()
    n_actual_nog = torch.sum(not_og_actual_indexes).item()
    print(n_matches_nog, n_matches_nog / n_predicted_nog, n_matches_nog / n_actual_nog)

    return


def main():
    # Generate csv file from exif data/raw data. it still needs to be changed later
    generateExifDataset()

    # Import csv data to a pytorch tensor
    exif_data = importCSVData()
    # print(exif_data.shape)

    # Before the permutation of the columns, we need to
    # check if the tensor is contiguous and turn it contiguous if it's not
    isContiguous = exif_data.is_contiguous()
    if not isContiguous:
        exif_data = exif_data.contiguous()

    # Permute the tensor columns
    desired_order = [
        37, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
        35, 36, 38, 39, 40, 41, 42, 43, 0, 44
    ]

    exif_data_permuted = exif_data[:, desired_order]  # get the desired order and permute columns

    # data = exif_data_permuted[:, :-1]  # all except the last column of each row
    # target = exif_data_permuted[:, -1]  # only the last column of each row

    checkImageData(exif_data_permuted)





    return


if __name__ == '__main__':
    timer_data(main)
