from auxiliary_func.getPath import get_base_path
import numpy as np
import torch
import csv


def importCSVData(csv_path):
    csv_data_numpy = np.loadtxt(
        csv_path,
        dtype=np.float32,
        delimiter=',',
        skiprows=1
    )
    return torch.from_numpy(csv_data_numpy)  # Returns a PyTorch Tensor


def main():
    base_path = get_base_path()
    filename = ''
    csv_img_path = f'{base_path}/ProjetoRedesNeurais/{filename}.csv'

    # import csv data to a pytorch tensor
    img_data = importCSVData(csv_img_path)

