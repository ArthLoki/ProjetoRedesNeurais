from exif import Image

import os

from ProjetoRedesNeurais.T1.auxiliary.readFiles import openImageFile

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

image_path = f'{editPath(current_path, 2)}/Images'.replace('\\', '/')
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']


def openImage(filename):
    with open(image_path + '/' + filename, 'rb') as img_file:
        img = Image(img_file)
    return img


def checkExifExistence(img):
    return img.has_exif


def listAllExifTags(img):
    return img.list_all()


def getExif(filename, tag):
    img = openImage(filename)
    if checkExifExistence(img):
        return img.get(tag)
    return None


def main():
    img = openImage(filenames[0])

    print(type(img))
    print(checkExifExistence(img))
    # print(listAllExifTags(img))

    return

main()
