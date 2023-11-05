# '/__pycache__/previousUrl.txt' and '/__pycache__/previousSearchResults.txt'
def storeFile(path, data):
    with open(path, 'w') as file:
        file.write(data)

def loadFileContent(path):
    try:
        with open(path, 'r') as file:
            ret = file.read()
            return ret
    except FileNotFoundError:
        return ''