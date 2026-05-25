import cv2
from analysis import findHorizontalCenterZeros
from utils import binarizeImage, calcBlackPixelsAlongHeight

def previewSplitLines(imagePath: str, afterPath: str = "test-after.jpg", lineColor: tuple = (0, 0, 255),) -> None:
    # Function draws lines horizontally. How it works ?
    # We get where to draw lines using findHorizontalCenterZeros() 
    # and draw them on the image for preview (without cropping)
    image = cv2.imread(imagePath)
    preview = image.copy()
    height, width = image.shape[:2]

    binaryImage = binarizeImage(imagePath)
    pixelCounts = calcBlackPixelsAlongHeight(binaryImage)
    horizontalSplitPoints = findHorizontalCenterZeros(pixelCounts)

    for y in horizontalSplitPoints:
        cv2.line(preview, (0, y), (width, y), lineColor, 2)

    cv2.imwrite(afterPath, preview)