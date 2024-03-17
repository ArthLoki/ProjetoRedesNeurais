import matplotlib.pyplot as plt

import os
import numpy as np

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath
from ProjetoRedesNeurais.T1.auxiliary.globalVariables import current_path

from ProjetoRedesNeurais.T1.image_analysis.compare_images import getPairsOfImagesAndExif
from ProjetoRedesNeurais.T1.exif.getExifExif import getExifDict

image_path = f'{editPath(current_path)}/Images'.replace("\\", "/")
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] in ['.jpg', '.jpeg']]


def create_or_update_dict(dict_data, key, data):
    if dict_data.get(key) is None:
        dict_data[key] = [data]
    else:
        dict_data[key].append(data)
    return dict_data


def get_dict_tags4statistcs():
    exif = getExifDict()
    pairs = getPairsOfImagesAndExif(exif)
    og_dict_tags = {}
    nog_dict_tags = {}

    for pair in pairs:
        for og, nog in pair.keys():
            value_pair = pair.get((og, nog))
            if value_pair is not None:
                for value in value_pair:
                    value_items = list(value.items())[0]

                    key = value_items[0]
                    og_data = value_items[1][0]
                    nog_data = value_items[1][1]

                    # if og_dict_tags.get(key) is None:
                    #     og_dict_tags[key] = [og_data]
                    # else:
                    #     og_dict_tags[key].append(og_data)
                    og_dict_tags = create_or_update_dict(og_dict_tags, key, og_data)

                    # if nog_dict_tags.get(key) is None:
                    #     nog_dict_tags[key] = [nog_data]
                    # else:
                    #     nog_dict_tags[key].append(nog_data)
                    nog_dict_tags = create_or_update_dict(nog_dict_tags, key, nog_data)

    return og_dict_tags, nog_dict_tags


def generateStatistics():
    og_dict_tags, nog_dict_tags = get_dict_tags4statistcs()

    for key, og_value in og_dict_tags.items():
        if og_value is None:
            og_value = 0

        nog_value = nog_dict_tags.get(key)
        if nog_value is None:
            nog_value = 0

        ogpoints = np.array(og_value)
        nogpoints = np.array(nog_value)

        if nogpoints is None:
            nogpoints = np.array([])

        plt.plot(ogpoints, color='blue')
        plt.plot(nogpoints, color='orange', linestyle='dotted')

        plt.title(key)

        plt.show()
    return


generateStatistics()
