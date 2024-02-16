from PIL import Image
from PIL.ExifTags import TAGS

import torch

from globalVariables import filenames, data_path


def getPillowExif(filename):
    image = Image.open('{}/{}'.format(data_path, filename))
    exif = image.getexif()
    image.close()
    return exif


def generatePillowExifDict():
    exif_dict = {}

    for filename in filenames:
        exif_table = getPillowExifTable(filename)
        exif_dict[filename] = exif_table

    return exif_dict


def getPillowExifTable(filename):
    exif = getPillowExif(filename)

    exif_table = {}

    for k, v in exif.items():
        tag = TAGS.get(k)
        exif_table[tag] = v
    return exif_table


# def getPillowExifTensor():
#     keys = []
#     all_values = []
#     exif_dict = generatePillowExifList()
#     for filename in exif_dict.keys():
#         exif = exif_dict[filename]
#         values = []
#         for k, v in exif.items():
#             if k not in keys:
#                 keys.append(k)
#             values.append(v)
#         all_values.append(values)
#     exif_tensor = torch.Tensor(all_values)
#     print(exif_tensor)
#     return


if __name__ == '__main__':
    exif_list = generatePillowExifDict()
    print(exif_list)
    # getPillowExifTensor()
