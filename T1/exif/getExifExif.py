from exif import Image

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import image_path, filenames


def openImage(filename):
    with open(image_path + '\\' + filename, 'rb') as img_file:
        img = Image(img_file)
    return img


def checkExifExistence(img):
    return img.has_exif


def listAllExifTags(img):
    return img.list_all()


def getExif(filename, tag):
    img = openImage(filename)
    if checkExifExistence(img):
        return img.tag
    return None


def main():
    img = openImage(filenames[0])
    print(listAllExifTags(img))

    return

main()