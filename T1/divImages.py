import os
from globalVariables import image_path
from exif.getPillowExif import generatePillowExifDict

og_images_filenames = [name for name in os.listdir(image_path)
                       if os.path.splitext(name)[-1] == '.jpg' and 'og_' in name]
nog_images_filenames = [name for name in os.listdir(image_path)
                        if os.path.splitext(name)[-1] == '.jpg' and 'og_' not in name]

# print(og_images_filenames)
# print(nog_images_filenames)


def getPairsOfImagesAndExif():

    # get pairs
    pairs = []
    dict_pillow_exif = generatePillowExifDict()
    for og_name in og_images_filenames:
        for nog_name in nog_images_filenames:
            pair = ({og_name: dict_pillow_exif.get(og_name)}, {nog_name: dict_pillow_exif.get(nog_name)})
            pairs.append(pair)
    return pairs


def main():
    pairs = getPairsOfImagesAndExif()
    print(pairs[0])
    return

main()
