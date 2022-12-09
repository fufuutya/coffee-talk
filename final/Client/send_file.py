import base64
def readIMG(filename):
    with open(filename, "rb") as f:
        file = f.read()
    return base64.b64encode(file).decode()

def writeIMG(path, string):
    with open(path, "wb") as f:
        f.write(base64.b64decode(string))