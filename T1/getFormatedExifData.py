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
global alphabet, str_data_indexes, dateIndexes, all_content
alphabet = [letter for letter in string.ascii_letters+string.punctuation.replace('.', '')+' ']
str_data_indexes = []
dateIndexes = []
all_content = []


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


def getMultSpecificIndexesFromContent(lInput, content):
    indexes = []
    for input in lInput:
        aux = getSpecificIndexesFromContent(input, content)
        for index in aux:
            if index not in indexes:
                indexes.append(index)
    return indexes


def getDateIndexes(content):
    global dateIndexes
    dateIndexes = sorted(getMultSpecificIndexesFromContent(['DateTime', 'Time', ':'], content))
    return tuple(dateIndexes)


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


def writeCSV(content, modo):
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


def generateExifDataset():
    global all_content, dateIndexes

    # Run this part only once to add header
    header = getHeaderList()
    dateIndexes = getDateIndexes(header)
    writeCSV(header, 'w')

    for i, filename in enumerate(filenames):
        content = getContentList(filename)

        str_data_indexes = findStrIndexes(content)
        print(f'str_data_indexes: {str_data_indexes}\ndateIndexes: {dateIndexes}')
        all_content.append(content)
        writeCSV(content, 'a')
    print('csv generated')

# Run if you want to test csv generation
# if __name__ == '__main__':
#     generateExifDataset()

