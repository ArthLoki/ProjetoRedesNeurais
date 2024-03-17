import exifread
import os

from PIL import Image
from PIL.ExifTags import TAGS

from ProjetoRedesNeurais.T1.auxiliary.readFiles import openImageFile

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

image_path = f'{editPath(current_path)}/Images'.replace('\\', '/')
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']

img_file = openImageFile(image_path, filenames[0])
tags = exifread.process_file(img_file)
serializable = dict(
                    [key, value] for key, value in tags.items())
print(serializable)


def _extract_exif(filename):
    ret = {}
    # ipdb.set_trace()
    img = Image.open(image_path + '/' + filename)
    info = img._getexif()
    date_format = "%Y:%m:%d %H:%M:%S"
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

        with open(image_path + '/' + filename, 'rb') as fimg:
            exif = exifread.process_file(fimg, details=False)

            serializable = dict(
                [key, value.printable] for key, value in exif.items())
            exif_json = serializable
            # ipdb.set_trace()
            if 'EXIF DateTimeOriginal' in exif.keys():
                tst_str = exif['EXIF DateTimeOriginal'].values
                try:
                    tst_dt = datetime.strptime(
                        tst_str, date_format).replace(tzinfo=pytz.utc)
                except:
                    tst_dt = None
                # ipdb.set_trace()
                exif_timestamp = tst_dt
            else:
                exif_timestamp = None


# print(_extract_exif(filenames[0]))
