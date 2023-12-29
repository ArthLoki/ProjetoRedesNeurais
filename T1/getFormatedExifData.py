import string
from ProjetoRedesNeurais.auxiliary_func.getPath import get_base_path
import os

from contertString2number import convertDinamicallyData

# Global variables
# 1 - Path
global base_path, data_path, csv_path, csv_total_path
base_path = get_base_path()
data_path = f'{base_path}/Images/T1'
csv_path = f'{base_path}/T1'

# 2 - Files
global filenames, csv_filename1, csv_filename2
filenames = [name for name in os.listdir(data_path) if os.path.splitext(name)[-1] == '.jpg']
csv_filename1 = 'output.csv'
csv_filename2 = 'original_dataset.csv'

# 3 - aux variables
global alphabet
alphabet = [letter for letter in string.ascii_letters+string.punctuation.replace('.', '')+' ']


# Funções
def getSpecificIndexes(input):
    file = openTXT(data_path, filenames[0])  # gets header from the first exif file
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


def getMultSpecificIndexesFromContent(lInput, content):
    indexes = []
    for input in lInput:
        aux = getSpecificIndexesFromContent(input, content)
        for index in aux:
            if index not in indexes:
                indexes.append(index)
    return indexes


def getDateIndexes(content):
    dateIndexes = sorted(getMultSpecificIndexesFromContent(['DateTime'], content))
    return tuple(dateIndexes)


def getOffsetTimeIndexes(content):
    offsetTimeIndexes = sorted(getMultSpecificIndexesFromContent(['OffsetTime'], content))
    return tuple(offsetTimeIndexes)


def getDivDataIndexes(content):
    divDataIndexes = sorted(getMultSpecificIndexesFromContent(['ShutterSpeed', 'Brightness', 'ExposureBias'], content))
    return tuple(divDataIndexes)


def findIndexFilePath():
    FilePathIndex = getSpecificIndexes('FilePath')
    return FilePathIndex[0]


def findStrIndexes(content):
    global str_data_indexes

    strIndexes = sorted(getMultSpecificIndexesFromContent(alphabet, content))
    # dateIndexes = getDateIndexes(content)

    # for i in dateIndexes:
    #     if i in strIndexes:
    #         strIndexes.remove(i)

    return tuple(strIndexes)


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


def writeCSV(content, modo, filename):
    file = open(csv_path+'/'+filename, modo)
    if type(content) == list:
        file.write(str(content[0]))
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


def generateExifDataset():
    all_content = []

    # Run this part only once to add header
    header = getHeaderList()

    dateIndexes = getDateIndexes(header)
    offsetTimeIndexes = getOffsetTimeIndexes(header)
    divDataIndexes = getDivDataIndexes(header)

    print(f'dateIndexes: {dateIndexes}\noffsetTimeIndexes: {offsetTimeIndexes}\ndivDataIndexes: {divDataIndexes}')

    writeCSV(header, 'w', csv_filename1)
    writeCSV(header, 'w', csv_filename2)

    for i, filename in enumerate(filenames):
        content = getContentList(filename)

        writeCSV(content, 'a', csv_filename2)

        str_data_indexes = findStrIndexes(content)
        content = convertDinamicallyData(content, str_data_indexes, dateIndexes, offsetTimeIndexes, divDataIndexes)
        # all_content.append(content)

        writeCSV(content, 'a', csv_filename1)
    print('csv generated')
    return


# Run if you want to test csv generation
if __name__ == '__main__':
    generateExifDataset()
