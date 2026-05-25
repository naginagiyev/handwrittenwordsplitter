from splitter import splitImage
from visualize import previewSplitLines

outputDir = "crops"
imagePath = "test-before.jpg"
afterPath = "test-after.jpg"

# If your writing is perfect (including word text images etc), use usePerfectDivide = False (findHorizontalCenterZeros())
# If your writing is not so perfect (there are tight and inclined lines or bad handwriting), use usePerfectDivide = True (perfectDividingPoints())
usePerfectDivide = False
runPreview = True
runSplit = True

if runPreview:
    previewSplitLines(imagePath, afterPath=afterPath)

if runSplit:
    # this part combine all functions and save divided words as separate images.
    count = splitImage(imagePath, outputDir, usePerfectDivide=usePerfectDivide)
    print(f"Saved {count} word image(s) to '{outputDir}/'")