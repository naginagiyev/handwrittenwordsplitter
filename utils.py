import cv2
import numpy as np

def binarizeImage(imagePath: str) -> np.ndarray:
    # code is used for binarize image (image only consist of black and white colors)
    colorImage = cv2.imread(imagePath)
    grayImage = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY)
    _, binaryImage = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binaryImage

def calcBlackPixelsAlongHeight(binaryImage: np.ndarray) -> list[int]:
    # calcBlackPixelsAlongHeight() function calculate pixels horizontally as it is shown in the upper image
    return [int(np.sum(binaryImage[y, :] == 0)) for y in range(binaryImage.shape[0])]

def calcBlackPixelsAlongWidth(binaryImage: np.ndarray) -> list[int]:
    # do the same thing for the width(columns)
    return [int(np.sum(binaryImage[:, x] == 0)) for x in range(binaryImage.shape[1])]

def cropLine(imagePath: str, margin: int = 2) -> str:
    # there are drawn lines before we divide it into the parts and this function is used to crop these lines.
    # it should be croped because algorithm recognize it as a word
    image = cv2.imread(imagePath)
    height = image.shape[0]
    croppedImage = image[margin:height - margin, :]
    cv2.imwrite(imagePath, croppedImage)
    return imagePath

def cropEmptySpaces(imagePath: str) -> str:
    # function to crop image that we apply algorithm from top, bottom, left and right until it reaches a black pixel.
    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    _, binaryImg = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    invertedImg = cv2.bitwise_not(binaryImg)
    nz = cv2.findNonZero(invertedImg)
    if nz is None:
        return imagePath
    x, y, w, h = cv2.boundingRect(nz)
    croppedImg = img[y:y + h, x:x + w]
    cv2.imwrite(imagePath, croppedImg)
    return imagePath