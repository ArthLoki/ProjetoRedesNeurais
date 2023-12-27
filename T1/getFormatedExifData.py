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


def getSpecificIndexes(input):
    file = openTXT(data_path, filenames[0])
    header = createContentList(file, 0)

    indexes = []
    for i, label in enumerate(header):
        if input in label:
            indexes.append(i)
    return indexes


def getMultSpecificIndexes(lInput):
    indexes = []
    for input in lInput:
        indexes.append(i for i in getSpecificIndexes(input) if i not in indexes)
    return indexes


def getDateIndexes():
    dateIndexes = getSpecificIndexes('Date')
    return dateIndexes


def findIndexFilePath():
    FilePathIndex = getSpecificIndexes('FilePath')
    return FilePathIndex[0]


def openTXT(path, filename):
    file_path = f'{path}/{filename}.txt'
    file = open(file_path, 'rb')

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

    content = processingData(content, 1)

    # if is_header:
    #     content = processingData(content, 2)

    if type(content) == list:
        file.write(content[0])
        for c in content[1:]:
            file.write(f';{c}')
        file.write('\n')
    file.close()
    return

def getHeaderList():
    file = openTXT(data_path, filenames[0])
    header = createContentList(file, 0)
    # file.close()
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
    # file.close()
    return content


def generateExifDataset():
    findIndexFilePath()
    getDateIndexes()

    # Run this part only once to add header
    header = getHeaderList()
    # print("Header: ", header)
    writeCSV(header, 'w')

    for filename in filenames:
        content = getContentList(filename)
        # print(f"Content ({filename}): ", content)
        writeCSV(content, 'a')


if __name__ == '__main__':
    generateExifDataset()

