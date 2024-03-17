from exif import Image

import os

from ProjetoRedesNeurais.T1.auxiliary.readFiles import openImageFile
from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path
from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

image_path = f'{editPath(current_path)}/Images'.replace('\\', '/')
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] in ['.jpg', '.jpeg']]
print(filenames)


def openImage(filename):
    try:
        # with open(image_path + '/' + filename, 'rb') as img_file:
        #     img = Image(img_file)
        # return img

        img = Image(image_path + '/' + filename)
        return img
    except Exception as e:
        print(f"Error opening image '{filename}': {e}")
        return None


def checkExifExistence(img):
    return img.has_exif


def listAllExifTags(img):
    return img.list_all()


def getExif(img, tag):
    if img is None:
        return None

    dict_data = {}
    try:
        if checkExifExistence(img):
            if tag != 'exif_version':
                exif_data = img.get(tag)
                # print(tag, type(exif_data))
                if exif_data is not None:
                    dict_data[tag] = exif_data
    except Exception as e:
        print(f"Error retrieving EXIF data for tag '{tag}': {e}")
    return dict_data


def get_dict_data(img, filename):
    # img = openImage(filename)
    all_tags = listAllExifTags(img)
    dict_data = {}
    for tag in all_tags:
        exif_data = getExif(img, tag)
        if exif_data is not None:
            if type(exif_data) == dict:
                dict_data[tag] = exif_data.get(tag)
            else:
                dict_data[tag] = exif_data
    return dict_data


def getExifDict():
    exif_dict = {}

    try:
        for filename in filenames:
            img = openImage(filename)
            exif_table = get_dict_data(img, filename)
            exif_dict[filename] = exif_table
        # return exif_dict
    except Exception as e:
        print(f"Error creating EXIF dict: {e}")
    return exif_dict


def main():
    img = openImage(filenames[0])
    # print(type(img))

    # print(len(filenames))
    # print(getExifDict())
    # print(len(getExifDict(img).keys()))

    return


main()
