from exif import Image

import os

from ProjetoRedesNeurais.T1.auxiliary.readFiles import openImageFile
from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path
from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

image_path = f'{editPath(current_path)}/Images'.replace('\\', '/')
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']


def openImage(filename):
    try:
        with open(image_path + '/' + filename, 'rb') as img_file:
            img = Image(img_file)
        return img
    except Exception as e:
        print(e)


def checkExifExistence(img):
    return img.has_exif


def listAllExifTags(img):
    return img.list_all()


def getExif(img, tag):
    # img = openImage(filename)
    if checkExifExistence(img):
        return img.get(tag)
    return None


def get_dict_data(img, filename):
    # img = openImage(filename)
    all_tags = listAllExifTags(img)
    dict_data = {}
    for tag in all_tags:
        dict_data[tag] = getExif(img, tag)
    return dict_data


def getExifDict(img):
    exif_dict = {}

    for filename in filenames:
        exif_table = get_dict_data(img, filename)
        exif_dict[filename] = exif_table

    return exif_dict

def main():
    img = openImage(filenames[0])

    # print(len(filenames))
    print(getExifDict(img))
    # print(len(getExifDict(img).keys()))

    return


main()
