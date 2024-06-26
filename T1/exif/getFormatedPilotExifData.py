import os

from ProjetoRedesNeurais.T1.auxiliary.printListData import printListDataContent, getIndex

from ProjetoRedesNeurais.T1.auxiliary.contertString2number import convertDinamicallyData

from ProjetoRedesNeurais.T1.auxiliary.readFiles import writeCSV, openTXT, moveFile, writeTXTfile

from ProjetoRedesNeurais.T1.auxiliary.getIndexesFunc import getPartiallyNumericIndexesFromContent, findIndexFilePath
from ProjetoRedesNeurais.T1.auxiliary.getIndexesFunc import findStrIndexes

from ProjetoRedesNeurais.T1.auxiliary.globalVariables import base_path, current_path
from ProjetoRedesNeurais.T1.auxiliary.globalVariables import csv_filename1, csv_filename2
from ProjetoRedesNeurais.T1.auxiliary.globalVariables import alphabet

from ProjetoRedesNeurais.auxiliary_func.getPath import editPath

image_path = f'{editPath(current_path)}/Images'.replace("\\", "/")
filenames = [name for name in os.listdir(image_path) if os.path.splitext(name)[-1] == '.jpg']

exif_path = f'{image_path}/exif_txt'


# According to escolha_tratamento, changes data
def processingData(content, escolha_tratamento):
    file = openTXT(image_path, filenames[0])  # gets header from the first exif file
    header = createContentList(file, 0)

    filePathIndex = findIndexFilePath(header)

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


def getOgColumnData():
    ogColumnList = []

    # 1 - check if 'og' is in each filename in this list. If so, append 1 to the ogColumnList, else append 0
    for i, name in enumerate(filenames):
        if 'og_' in name:
            ogColumnList.append(1.0)
        else:
            ogColumnList.append(0.0)

    # 2 - create a tensor containing the content of ogColumnList
    # tensor = torch.tensor(ogColumnList)

    # 3  - return
    return ogColumnList


# Gets the list of labels in header
def getHeaderList():
    file = openTXT(image_path, filenames[0])  # gets header from the first exif file
    header = createContentList(file, 0)
    header = processingData(header, 1)
    file.close()
    return header

    # csv_exif = csv.reader(open(image_path), delimiter=";")
    # col_list = next(csv_exif)
    # return col_list


def cleanDataContentList(lData):
    lDataFixed = []
    # print(lData)
    for i in range(len(lData)):
        lDataFixed.append(lData[i].split('\"')[1])
    return lDataFixed


# creates a list from the data in the file. The param content_type refers to what kind of list you'll return
def createContentList(file, content_type):
    content = []
    for line in file:
        lData = str(line).strip().split(',')
        lData = cleanDataContentList(lData)

        # print(line, lData)

        if content_type == 0:  # wants to get header list
            content.append(lData[0])
        elif content_type == 1:
            content.append(lData[1])  # wants to get data list
        else:
            print("Escolha um tipo valido")
            exit(0)
    return content


def getContentList(filename):
    file = openTXT(image_path, filename)

    header = getHeaderList()

    content = createContentList(file, 1)
    content = processingData(content, 1)
    file.close()
    return content


def generateExifDataset():

    # Run this part only once to add header
    header = getHeaderList()
    header.append('OriginalImage')
    ogColumnData = getOgColumnData()

    # for i, name in enumerate(header):
    #     print('{:6}: {:100}'.format(i, name))
    # print('\n')

    writeCSV(header, 'w', csv_filename1, current_path)

    writeCSV(header, 'w', csv_filename2, current_path)

    for i, filename in enumerate(filenames):
        content = getContentList(filename)
        content.append(str(ogColumnData[i]))

        writeCSV(content, 'a', csv_filename2, current_path)

        dateIndexes = getPartiallyNumericIndexesFromContent(content, 2, 1)
        offsetTimeIndexes = getPartiallyNumericIndexesFromContent(content, 0, 1)
        divDataIndexes = getPartiallyNumericIndexesFromContent(content, 1, 0)
        str_data_indexes = findStrIndexes(content)
        writeTXTfile('str_data_indexes', 'File {} ({}): '.format(filename, i), 'a')
        writeTXTfile('str_data_indexes', '{}\n'.format(str_data_indexes), 'a')
        # print('Str indexes from line {}: {}'.format(i, str_data_indexes))

        content = convertDinamicallyData(
            content,
            str_data_indexes,
            dateIndexes,
            offsetTimeIndexes,
            divDataIndexes
        )

        writeCSV(content, 'a', csv_filename1, current_path)
    print('csv generated')
    return


# Run if you want to test csv generation
if __name__ == '__main__':
    generateExifDataset()
