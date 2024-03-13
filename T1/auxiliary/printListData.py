def printListDataContent(lista):
    for i, el in enumerate(lista):
        print(f'{i} - {el}')
    print('\n')
    return


def getIndex(lista, input):
    for i, el in enumerate(lista):
        if input in el:
            print(f'{i} - {el}')
            return i
