from ProjetoRedesNeurais.LabGPSI.auxiliary.getPath import get_base_path
import os
import string

# Global variables
# 1 - Path
global base_path, current_path
current_path = os.getcwd().replace('\\', '/')
base_path = get_base_path()

# 2 - Files
global filenames, csv_filename1, csv_filename2
csv_filename1 = 'output.csv'
csv_filename2 = 'original_dataset.csv'

# 3 - aux variables
global alphabet
alphabet = [letter for letter in string.ascii_letters+string.punctuation.replace('.', '')+' ']
