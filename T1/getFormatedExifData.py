from ProjetoRedesNeurais.auxiliary_func.getPath import get_base_path
import os

def readTXT(path, filename):
    file_path = f'{path}/{filename}.txt'
    file = open(file_path, 'rb')

    return file


def fixDataContentList(lData):
    lDataFixed = []
    for i in range(len(lData)):
        lDataFixed.append(lData[i].split('\"')[1])
    return lDataFixed


def createContentList(file, content_type):
    content = []
    for line in file:
        lData = str(line).strip().split(',')
        lData = fixDataContentList(lData)
        # print(f'lData: {lData}')

        if content_type == 0:  # wants to get header list
            # print(f'header: {lData[0]}')
            content.append(lData[0])
        elif content_type == 1:
            # print(f'data: {lData[1]}')
            content.append(lData[1])  # wants to get data list
        else:
            print("Escolha um tipo valido")
    return content


def writeCSV(path, filename, content, modo, is_exif_data=True):
    file = open(f'{path}/{filename}.csv', modo)

    if is_exif_data and modo == 'a':
        content[0] = content[0].replace('\\\\', '/')

    if type(content) == list:
        file.write(content[0])
        for c in content[1:]:
            file.write(f';{c}')
        file.write('\n')
    file.close()
    return


def getPathIndexes(header):
    pathIndexes = []
    for i in header:
        if header[i].endsith('Path'):
            pathIndexes.append(i)
    return pathIndexes


def main():
    base_path = get_base_path()
    data_path = f'{base_path}/Images/T1'
    csv_path = f'{base_path}/T1'

    filenames = [name for name in os.listdir(data_path) if os.path.splitext(name)[-1] == '.jpg']

    # Run this part only once to add header
    file = readTXT(data_path, filenames[0])
    header = createContentList(file, 0)
    writeCSV(csv_path, 'output', header, 'w', False)

    for filename in filenames:
        file = readTXT(data_path, filename)
        content = createContentList(file, 1)
        writeCSV(csv_path, 'output', content, 'a', True)

    file.close()


if __name__ == '__main__':
    main()

