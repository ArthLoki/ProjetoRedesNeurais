import cv2
import os
import exifread

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path

image_path = f'{editPath(current_path)}/Images'.replace("\\", "/")
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']


def get_total_img_path(filename):
    return image_path + '/' + filename


def get_exif_data(filename):
    # Leitura da imagem usando OpenCV
    img_path = get_total_img_path(filename)
    image = cv2.imread(img_path)
    print(image.shape)  # (6000, 8000, 3) = (altura, comprimento, canal de cor [no formato BRG (blue, red, green)])

    # Abertura do arquivo da imagem em modo de leitura binária
    with open(img_path, 'rb') as f:
        # Passagem do arquivo para a função exifread
        tags = exifread.process_file(f)

    dict_data = {}
    if tags:
        # print("EXIF data:")
        for tag, value in tags.items():
            # print(f"Tag: {tag}, Value: {value}")
            dict_data[tag] = value
    else:
        print("No EXIF data found.")

    print(len(dict_data.keys()))

    return dict_data


if __name__ == "__main__":
    get_exif_data(filenames[0])
