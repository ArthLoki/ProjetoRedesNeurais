import Exif
import os

from ProjetoRedesNeurais.T1.auxiliary.readFiles import openImageFile

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

image_path = f'{editPath(current_path, 1)}/Images'.replace('\\', '/')
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']
