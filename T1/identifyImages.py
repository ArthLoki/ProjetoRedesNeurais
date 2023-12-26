from ProjetoRedesNeurais.auxiliary_func.getPath import get_base_path
from ProjetoRedesNeurais.auxiliary_func.getTimer import timer_data
import numpy as np
import torch
import csv
import os

global base_path, data_path
base_path = get_base_path()
data_path = f'{base_path}/ProjetoRedesNeurais'


def importCSVData(csv_path):
    csv_data_numpy = np.loadtxt(
        csv_path,
        dtype=np.float32,
        delimiter=';',
        skiprows=1
    )
    return torch.from_numpy(csv_data_numpy)  # Returns a PyTorch Tensor


def getImageIdentifierColumnList():
    global data_path

    data_dir = f'{data_path}/Images/T1'
    imageIdentifierColumnList = [name for name in os.listdir(data_dir) if os.path.splitext(name)[-1] == '.jpg']

    return imageIdentifierColumnList


def getOgColumnList():
    ogColumnList = []

    # 1 - get image filenames, creating a list
    imageIdentifierColumnList = getImageIdentifierColumnList()

    # 2 - check if 'og' is in each filename in this list. If so, append 1.0 to the ogColumnList, else append 0.0
    for name in imageIdentifierColumnList:
        if 'og' in name:
            ogColumnList.append(1.0)
        else:
            ogColumnList.append(0.0)

    # 3 - return ogColumnList
    return ogColumnList


def main():
    global data_path
    filename = 'output.csv'
    csv_img_path = f'{base_path}/T1/{filename}'

    # import csv data to a pytorch tensor
    # img_data = importCSVData(f'C:/Users/lubjc/PycharmProjects/DeepLearning/ProjetoRedesNeurais/T1/{filename}')
    img_data = importCSVData(csv_img_path)
    print(img_data.shape)


if __name__ == '__main__':
    main()

