# TODO: Tudo o que não consegui fazer com Torch (T<num>) ou Numpy (N<num>) e outras partes (O<num>)
# N1 - Usar o converters do loadtxt para converter string para numeric
# T1 - Adicionar coluna booleana chamada de OriginalImage usando torch.Tensor.scatter_


from ProjetoRedesNeurais.auxiliary_func.getTimer import timer_data

import numpy as np
import torch
import os

from getFormatedExifData import generateExifDataset, getSpecificIndexes, getHeaderList, findStrIndexes
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


# noinspection DuplicatedCode
def checkImageData(exif_data_permuted):
    data = exif_data_permuted[:, :-1]  # all except the last column of each row
    target = exif_data_permuted[:, -1]  # only the last column of each row

    col_list = getHeaderList()

    og_data = data[target == 1.0]
    not_og_data = data[target != 1.0]

    og_mean = torch.mean(og_data, dim=0)
    nog_mean = torch.mean(not_og_data, dim=0)

    # for i, args in enumerate(zip(col_list, og_mean, nog_mean)):
    #     diff = args[1].tolist() - args[2].tolist()
    #     print('{:2} - {:20}\t\t{:6.2f}\t\t{:6.2f}\t\t{:6.2f}'.format(i, *args, diff))

    # The original images seems to have a higher /Exif/Image/YResolution (7), /Exif/Photo/FocalLength (28)
    # Meanwhile, the called 'not original images' seems to have higher /Exif/Photo/MaxAperture (25),
    # /Exif/Photo/MeteringMode (26)

    for i in range(len(col_list)):
        # print('\n\n---> COLUMN {:6}'.format(i))
        writeTXTfile('data_analysis', '\n---> COLUMN {} ({})'.format(col_list[i], i), 'a')

        # Finding original images
        og_predicted_indexes = getPredictedIndexes(data, og_mean, i, 'less than')

        # Finding 'not original' images
        nog_predicted_indexes = getPredictedIndexes(data, nog_mean, i, 'greater than')

        # the indexes of the images
        og_actual_indexes = target == 1.0
        # print(og_actual_indexes.sum())

        nog_actual_indexes = target != 1.0
        # print(nog_actual_indexes.sum())

        # Comparing actual original images
        # print('\n\n>>> Original Images')
        writeTXTfile('data_analysis', '\n>>> Original Images', 'a')
        getResults(og_actual_indexes, og_predicted_indexes)

        # Comparing not original images
        # print('\n\n>>> Not Original Images')
        writeTXTfile('data_analysis', '\n>>> Not Original Images', 'a')
        getResults(nog_actual_indexes, nog_predicted_indexes)

        # print('\n')

    return


def writeTXTfile(filename, content, modo):
    file = open('{}.txt'.format(filename), modo)
    file.write('{}'.format(content))
    file.close()


def getPredictedIndexes(data, data_mean, index, modo='greater than'):
    img_threshold = data_mean[index].float()
    img_data = data[:, index]

    predicted_indexes = torch.gt(img_data, img_threshold)

    if modo != 'greater than':
        if modo == 'greater than or equal':
            predicted_indexes = torch.ge(img_data, img_threshold)
        elif modo == 'less than':
            predicted_indexes = torch.lt(img_data, img_threshold)
        elif modo == 'less than or equal':
            predicted_indexes = torch.le(img_data, img_threshold)

    return predicted_indexes


def getResults(actual_indexes, predicted_indexes):
    n_matches = torch.sum(actual_indexes & predicted_indexes).item()
    n_predicted = torch.sum(predicted_indexes).item()
    n_actual = torch.sum(actual_indexes).item()

    # print(n_matches, n_predicted, n_actual)
    writeTXTfile('data_analysis', '\nMatches: {}\nPredicted: {}\nActual: {}\n'.format(n_matches, n_predicted, n_actual), 'a')

    if n_predicted != 0:
        predicted_actual = n_predicted / n_actual
        matches_predicted = n_matches / n_predicted
        matches_actual = n_matches / n_actual

        # print('Number of matches: {:3}'.format(n_matches))
        # print('% of n_predicted / n_actual: {:6.2f}'.format(n_predicted / n_actual))
        # print('% of n_matches / n_predicted: {:6.2f}'.format(n_matches / n_predicted))
        # print('% of n_matches / n_actual: {:6.2f}'.format(n_matches / n_actual))

        # writeTXTfile('data_analysis', '\nNumber of matches: {:3}'.format(n_matches), 'a')
        writeTXTfile('data_analysis', '\n% of n_predicted / n_actual: {:.2f}'.format(predicted_actual), 'a')
        writeTXTfile('data_analysis', '\n% of n_matches / n_predicted: {:.2f}'.format(matches_predicted), 'a')
        writeTXTfile('data_analysis', '\n% of n_matches / n_actual: {:.2f}\n\n'.format(matches_actual), 'a')
    return


def main():
    # Generate csv file from exif data/raw data. it still needs to be changed later
    # generateExifDataset()

    # Import csv data to a pytorch tensor
    exif_data = importCSVData()
    # print(exif_data.shape)

    # Before the permutation of the columns, we need to
    # check if the tensor is contiguous and turn it contiguous if it's not
    # isContiguous = exif_data.is_contiguous()
    # if not isContiguous:
    #     exif_data = exif_data.contiguous()

    # Permute the tensor columns
    desired_order = [
        37, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
        35, 36, 38, 39, 40, 41, 42, 43, 0, 44
    ]

    exif_data_permuted = exif_data[:, desired_order]  # get the desired order and permute columns

    checkImageData(exif_data_permuted)

    return


if __name__ == '__main__':
    timer_data(main)
