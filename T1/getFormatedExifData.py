import string
from ProjetoRedesNeurais.auxiliary_func.getPath import get_base_path
import os

# Global variables
# 1 - Path
global base_path, data_path, csv_path, csv_total_path
base_path = get_base_path()
data_path = f'{base_path}/Images/T1'
csv_path = f'{base_path}/T1'

# 2 - Files
global filenames, csv_filename
filenames = [name for name in os.listdir(data_path) if os.path.splitext(name)[-1] == '.jpg']
csv_filename = 'output.csv'
csv_total_path = f'{csv_path}/{csv_filename}'

# 3 - aux variables
global alphabet, str_data_indexes
alphabet = [letter for letter in string.ascii_letters+string.punctuation.replace('.', '')+' ']
str_data_indexes = []


# Funções
def getSpecificIndexes(input):
    file = openTXT(data_path, filenames[0])
    header = createContentList(file, 0)

    indexes = []
    for i, label in enumerate(header):
        if input in label:
            indexes.append(i)
    return indexes


def getSpecificIndexesFromContent(input, content):
    indexes = []
    for i, data in enumerate(content):
        if input in data:
            indexes.append(i)
    return indexes


def getMultSpecificIndexes(lInput, content):
    indexes = []
    for input in lInput:
        aux = getSpecificIndexesFromContent(input, content)
        for index in aux:
            if index not in indexes:
                indexes.append(index)
    return indexes


def getDateIndexes(content):
    dateIndexes = getMultSpecificIndexes(['DateTime', ':'], content)
    return dateIndexes


def findIndexFilePath():
    FilePathIndex = getSpecificIndexes('FilePath')
    return FilePathIndex[0]


def findStrIndexes(content):
    strIndexes = sorted(getMultSpecificIndexes(alphabet, content))

    dateIndexes = getDateIndexes(content)
    for i in dateIndexes:
        if i in strIndexes:
            strIndexes.remove(i)

    return strIndexes


def openTXT(path, filename):
    file_path = f'{path}/{filename}.txt'
    file = open(file_path, 'r')

    return file


def processingData(content, escolha_tratamento):
    filePathIndex = findIndexFilePath()

    if escolha_tratamento == 0:
        # Replaces \\ to /
        content[filePathIndex] = content[filePathIndex].replace('\\\\', '/')
    if escolha_tratamento == 1:
        # Removes the FilePath data from dataset
        content.pop(filePathIndex)
    elif escolha_tratamento == 2:
        # Makes the header label shorter
        for i, h in enumerate(content):
            content[i] = h.split('/')[-1]
    return content


def writeCSV(content, modo, is_header=False):
    file = open(csv_total_path, modo)
    if type(content) == list:
        file.write(content[0])
        for c in content[1:]:
            if c == '<undefined>':
                file.write(f';{0}')
            else:
                file.write(f';{c}')
        file.write('\n')
    file.close()
    return

def getHeaderList():
    file = openTXT(data_path, filenames[0])
    header = createContentList(file, 0)
    header = processingData(header, 1)
    file.close()
    return header


def cleanDataContentList(lData):
    lDataFixed = []
    for i in range(len(lData)):
        lDataFixed.append(lData[i].split('\"')[1])
    return lDataFixed


def createContentList(file, content_type):
    content = []
    for line in file:
        lData = str(line).strip().split(',')
        lData = cleanDataContentList(lData)

        if content_type == 0:  # wants to get header list
            content.append(lData[0])
        elif content_type == 1:
            content.append(lData[1])  # wants to get data list
        else:
            print("Escolha um tipo valido")
    return content


def getContentList(filename):
    file = openTXT(data_path, filename)
    content = createContentList(file, 1)
    content = processingData(content, 1)
    file.close()
    return content

# Main
def generateExifDataset():
    global str_data_indexes

    # Run this part only once to add header
    header = getHeaderList()
    writeCSV(header, 'w')

    for filename in filenames:
        content = getContentList(filename)
        str_data_indexes.append(findStrIndexes(content))
        writeCSV(content, 'a')
    print('csv generated')


# if __name__ == '__main__':
#     generateExifDataset()

