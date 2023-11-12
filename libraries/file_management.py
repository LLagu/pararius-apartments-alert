import os

def storeFile(path, data):
    absolute_path = os.path.abspath(path)
    with open(absolute_path, 'w') as file:
        file.write(data)


def loadFileContent(path):
    try:
        absolute_path = os.path.abspath(path)
        with open(absolute_path, 'r') as file:
            ret = file.read()
            return ret
    except FileNotFoundError:
        return ''
