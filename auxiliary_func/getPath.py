import os


def get_current_path():
    return os.getcwd().replace('\\', '/')


def get_base_path():
    og_path = get_current_path()
    l_path = og_path.split('/')
    base_path = l_path[0]
    for i in range(1, len(l_path)-1):
        base_path += f'/{l_path[i]}'
    return base_path


def editPath(ogpath, backspace):

    if backspace > 0:
        dirs = ogpath.split('/')
        edited_path = f'{dirs[0]}'
        for d in dirs[1:-backspace]:
            edited_path += f'\\{d}'
        return edited_path
    return ogpath
