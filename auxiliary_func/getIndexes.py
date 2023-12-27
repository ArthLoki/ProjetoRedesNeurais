from ProjetoRedesNeurais.T1.getFormatedExifData import openTXT, createContentList


def getSpecificIndexes(input):
    file = openTXT(data_path, filenames[0])
    header = createContentList(file, 0)

    indexes = []
    for label in header:
        if input in label:
            indexes.append(i)
    return indexes


def getMultSpecificIndexes(lInput, content):
    indexes = []
    for input in lInput:
        indexes.append(i for i in getSpecificIndexes(input) if i not in indexes)
    return indexes


def getDateIndexes():
    dateIndexes = getSpecificIndexes('Date')
    print(dateIndexes)
    return


def findIndexFilePath():
    FilePathIndex = getSpecificIndexes('FilePath')
    print(FilePathIndex)
    return