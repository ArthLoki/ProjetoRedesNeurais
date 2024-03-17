import os
from skimage import io
from PIL import Image
from PIL.ExifTags import TAGS

from matplotlib import pyplot as plt

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path

image_path = f'{editPath(current_path)}/Images'.replace("\\", "/")
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']


def get_total_img_path(filename):
    return image_path + '/' + filename


def get_exif_data(filename):
    # Read the image using scikit-image
    img_path = get_total_img_path(filename)
    image = io.imread(img_path)
    print(image.shape)  # (6000, 8000, 3) = (altura, comprimento, canal de cor [no formato BRG (blue,red, green)])

    # Open the image using Pillow to access EXIF data
    pil_image = Image.open(img_path)
    exif_data = pil_image._getexif()

    # Map the tag numbers to tag names
    tag_names = {TAGS.get(tag): value for tag, value in exif_data.items()}
    print(len(tag_names.keys()))

    return tag_names


get_exif_data(filenames[0])