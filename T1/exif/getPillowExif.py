from PIL import Image
from PIL.ExifTags import TAGS

from ProjetoRedesNeurais.T1.auxiliary.readFiles import writeCSV

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import filenames, image_path, csv_path


def getPillowExif(filename):
    image = Image.open('{}/{}'.format(image_path, filename))
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


def generatePillowExifCSV(original_filename, converted_filename):
    # {filename: {attr1: value1, attr2: value2, ...}}

    exif_dict = generatePillowExifDict()

    img_name = list(exif_dict.keys())

    header = ['Filename']
    header.extend(list((exif_dict.get(img_name[0])).keys()))

    writeCSV(header, 'w', original_filename, csv_path)
    writeCSV(header, 'w', converted_filename, csv_path)

    for name in img_name:
        content = [name]
        content.extend(list((exif_dict.get(name)).values()))
        writeCSV(content, 'a', original_filename, csv_path)


    # TODO: it needs to be converted to float32 to generate statistics
    return


if __name__ == '__main__':
    exif_list = generatePillowExifDict()
    # print(exif_list)

    generatePillowExifCSV('../original_pillow_exif_dataset.csv', '../output_pillow_exif_dataset.csv')
