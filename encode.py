import os
from PIL import Image

def getNumInRange(message, min, max):
    while True:
        try:
            num = int(input(message).strip())
            if (num >= min) and (num <= max):
                os.system('cls' if os.name == 'nt' else 'clear')
                return num
            else:
                print("Value error, Please enter a valid value")
        except ValueError:
            print("Value error, Please enter a valid value")
            continue

def getImage():
    while True:
        img = input("Enter image path + name + extension:\n>>> ")
        if (os.path.exists(img)):
            return Image.open(img, 'r')
        print("Image wasn't found, please try again.")

def getFormat():
    print("1: png, 2: tiff.")
    if (getNumInRange("Please choose format for your image.\n>>> ", 1, 2) == 1):
        return ".png"
    return ".tiff"

def genData(data):
    newd = []
    for value in data:
        newd.append(format(ord(value), '08b'))
    return newd

def modPix(encodedImgData, message):
    dataList = genData(message)
    dataLength = len(dataList)
    indexRGBcode = iter(encodedImgData)
    for i in range(dataLength):
        encodedImgData = [value for value in indexRGBcode.__next__()[:3] + indexRGBcode.__next__()[:3] + indexRGBcode.__next__()[:3]]
        for j in range(0, 8):
            if (dataList[i][j] == '0') and (encodedImgData[j] % 2 != 0):
                encodedImgData[j] -= 1
            elif (dataList[i][j] == '1') and (encodedImgData[j] % 2 == 0):
                encodedImgData[j] -= 1
        if (i == dataLength - 1) and (encodedImgData[-1] % 2 == 0):
            encodedImgData[-1] -= 1
        elif (encodedImgData[-1] % 2 != 0):
            encodedImgData[-1] -= 1
        encodedImgData = tuple(encodedImgData)
        yield encodedImgData[0:3]
        yield encodedImgData[3:6]
        yield encodedImgData[6:9]

def encodeEnc(encodedImg, message):
    size = encodedImg.size[0]
    x, y = 0, 0
    for pixel in modPix(encodedImg.getdata(), message):
        encodedImg.putpixel((x, y), pixel)
        if (x == size - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode():
    image = getImage()
    message = input("Enter message to encode:\n>>> ").strip()
    while (len(message) == 0):
        message = input("Nothing was entered, please enter a message:\n>>> ").strip()
    encodedImg = image.copy()
    encodeEnc(encodedImg, message)
    newImageName = input("Enter the name of the new image without extension!:\n>>> ").strip()
    while (len(newImageName) == 0):
        newImageName = input("Nothing was entered, please enter a name for the new image:\n>>> ").strip()
    newImageName += getFormat()
    encodedImg.save(newImageName, str(newImageName.split(".")[1]))

def decode():
    image = getImage()
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        binstr = ''
        for binaryPixelValue in pixels[:8]:
            if (binaryPixelValue % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    whatFunction2Run = getNumInRange("Press 1 to encode & 2 for decode.\n>>> ", 1, 2)
    if (whatFunction2Run == 1):
        encode()
    else:
        print("Decoded message:\n>>> " + decode())

main()
