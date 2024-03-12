from ProjetoRedesNeurais.auxiliary_func.getPath import get_base_path
import os
import string

# Global variables
# 1 - Path
global base_path, data_path, csv_path, exif_path, current_path
base_path = get_base_path()
data_path = f'{base_path}/Images/T1'
exif_path = f'{data_path}/exif_txt'
csv_path = f'{base_path}/T1'

current_path = os.getcwd().replace('\\', '/')

# 2 - Files
global filenames, csv_filename1, csv_filename2
filenames = [name for name in os.listdir(data_path) if os.path.splitext(name)[-1] == '.jpg']
csv_filename1 = 'output.csv'
csv_filename2 = 'original_dataset.csv'

# 3 - aux variables
global alphabet
alphabet = [letter for letter in string.ascii_letters+string.punctuation.replace('.', '')+' ']
