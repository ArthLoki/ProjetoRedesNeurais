from skimage import io
from skimage.transform import resize, rescale, downscale_local_mean

from matplotlib import pyplot as plt

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import image_path, filenames

path = '{}\\{}'.format(image_path, filenames[0])
print(path)

# img = io.imread('{}\\{}'.format(image_path, filenames[0]), as_grey=True)
