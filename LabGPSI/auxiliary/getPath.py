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


def editPath(ogpath):
    backspace = get_backspace(ogpath, 'ProjetoRedesNeurais')
    if backspace > 0:
        dirs = ogpath.split('/')
        edited_path = f'{dirs[0]}'
        for d in dirs[1:-backspace]:
            edited_path += f'/{d}'
        return edited_path
    return ogpath


def get_backspace(og_path, chosen_directory):
    dirs = og_path.split('/')

    if dirs:
        if chosen_directory in dirs:
            i = dirs.index(chosen_directory)

            if i <= len(dirs)-1:
                return len(dirs)-i-1
            else:
                return 0
        else:
            new_path = dirs[0]
            for d in dirs[1:-1]:
                new_path += '/{}'.format(d)
            return get_backspace(new_path, chosen_directory)
    else:
        return 0
