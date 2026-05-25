import os
import cv2
import tempfile
import numpy as np
from toolz import pipe

from analysis import (
    findHorizontalCenterZeros,
    findMostChange,
    findVerticalCenterZeros,
    perfectDividingPoints,
    zeroSequenceLengths,
)

from utils import (
    binarizeImage,
    calcBlackPixelsAlongHeight,
    calcBlackPixelsAlongWidth,
    cropEmptySpaces,
    cropLine,
)

def _getHorizontalSplitPoints(imagePath: str, usePerfectDivide: bool) -> list[int]:
    # as I mentioned before there is two functions to divide text into words:
    # If your writing is perfect(including word text images etc), use findHorizontalCenterZeros()
    # If your writing is not soo perfect (there are tight and inclined lines or bad handwriting), use perfectDividingPoints()
    binaryImage = binarizeImage(imagePath)
    pixelCounts = calcBlackPixelsAlongHeight(binaryImage)
    if usePerfectDivide:
        return perfectDividingPoints(pixelCounts, imagePath)
    return findHorizontalCenterZeros(pixelCounts)

def _getVerticalSplitPoints(imagePath: str) -> list[int]:
    binaryImage = binarizeImage(imagePath)
    pixelCounts = calcBlackPixelsAlongWidth(binaryImage)
    spaceLimit = pipe(
        pixelCounts,
        zeroSequenceLengths,
        lambda x: sorted(set(x)),
        findMostChange,
    )
    return findVerticalCenterZeros(pixelCounts, spaceLimit)

def _cropHorizontalSegments(imagePath: str, splitPoints: list[int]) -> list[np.ndarray]:
    # crop the image at each horizontal dividing point (from findHorizontalCenterZeros() or perfectDividingPoints())
    image = cv2.imread(imagePath)
    segments = []
    boundaries = [0] + splitPoints + [image.shape[0]]
    for i in range(len(boundaries) - 1):
        segment = image[boundaries[i]:boundaries[i + 1], :]
        segments.append(segment)
    return segments

def _cropVerticalSegments(imagePath: str, splitPoints: list[int]) -> list[np.ndarray]:
    # crop the image at each vertical dividing point (from findVerticalCenterZeros())
    image = cv2.imread(imagePath)
    segments = []
    boundaries = [0] + splitPoints + [image.shape[1]]
    for i in range(len(boundaries) - 1):
        segment = image[:, boundaries[i]: boundaries[i + 1]]
        segments.append(segment)
    return segments

def splitImage(imagePath: str, outputDir: str, usePerfectDivide: bool = False) -> int:
    # this part combine all functions and save divided words as separate images.
    os.makedirs(outputDir, exist_ok=True)
    horizontalSplitPoints = _getHorizontalSplitPoints(imagePath, usePerfectDivide)
    lineSegments = _cropHorizontalSegments(imagePath, horizontalSplitPoints)

    wordIndex = 0
    for lineImg in lineSegments:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmpPath = tmp.name

        try:
            cv2.imwrite(tmpPath, lineImg)
            cropLine(tmpPath)
            cropEmptySpaces(tmpPath)

            verticalSplitPoints = _getVerticalSplitPoints(tmpPath)
            wordSegments = _cropVerticalSegments(tmpPath, verticalSplitPoints)

            for wordImg in wordSegments:
                outputPath = os.path.join(outputDir, f"word_{wordIndex:04d}.jpg")
                cv2.imwrite(outputPath, wordImg)
                wordIndex += 1
        except Exception:
            continue
        finally:
            if os.path.exists(tmpPath):
                os.remove(tmpPath)

    return wordIndex