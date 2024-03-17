import os
from ProjetoRedesNeurais.auxiliary_func.getPath import editPath
from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path
from ProjetoRedesNeurais.T1.exif.getPillowExif import generatePillowExifDict
from ProjetoRedesNeurais.T1.exif.getExifExif import getExifDict

image_path = f'{editPath(current_path)}/Images'.replace("\\", "/")
# print(image_path)

og_images_filenames = [name for name in os.listdir(image_path)
                       if os.path.splitext(name)[-1] in ['.jpg', '.jpeg'] and 'og_' in name]
nog_images_filenames = [name for name in os.listdir(image_path)
                        if os.path.splitext(name)[-1] in ['.jpg', '.jpeg'] and 'og_' not in name]


def getPairsOfImagesAndExif(dict_exif):
    # {(og_name, nog_name): {attr1: (og, nog), attr2: (og, nog), ...}}

    # get pairs
    pairs = []
    for og_name in og_images_filenames:
        for nog_name in nog_images_filenames:
            if nog_name in og_name:
                header = list(dict_exif.get(og_name).keys())

                key_pair = (og_name, nog_name)
                value_pair = [{i: (dict_exif.get(og_name).get(i), dict_exif.get(nog_name).get(i))}
                              for i in header]
                pair = {key_pair: value_pair}
                pairs.append(pair)
    return pairs


def main():
    # dict_pillow_exif = generatePillowExifDict()
    dict_exif = getExifDict()
    pairs = getPairsOfImagesAndExif(dict_exif)
    # print(type(pairs))
    # print(pairs[0])
    return


if __name__ == '__main__':
    main()
