import os

from skimage import io
from skimage.transform import resize, rescale, downscale_local_mean

from matplotlib import pyplot as plt

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path

image_path = f'{editPath(current_path, 3)}/Images'.replace("\\", "/")
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']

path = image_path + '/' + filenames[0]
print(path)
