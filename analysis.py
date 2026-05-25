from PIL import Image

def zeroSequenceLengths(lst: list[int]) -> list[int]:
    # find the lengths of each zero sequences in a list and append its length into a new list. 
    # For example :
    # [0, 0, 0, 1, 2, 3, 0, 0, 4, 5, 6, 0, 0, 0, 0]
    # This function return [3, 2, 4] (the lengths of each zero sequence orderly)
    # this function used calculate length of 0 sequences and 
    # then we'll find which spacings are between letters and 
    # which one between words using findMostChange() function
    zeroLengths = []
    count = 0
    for num in lst:
        if num == 0:
            count += 1
        elif count > 0:
            zeroLengths.append(count)
            count = 0
    if count > 0:
        zeroLengths.append(count)
    return zeroLengths

def findMostChange(points: list[int]) -> int:
    # is used to find, after which number in a list most change happens, for example :
    # [2, 5, 11, 19]
    # in this case, our function will return 11, beacuse most difference is between 11 and 19
    # Between 2 and 5, it is 3. Between 5 and 11, it is 6. Between 11 and 19, it is 8.
    # This function is used, when we divide lines into to the words, to select if it is space between letters or space between words.
    # It take function's return as limit. If space is smaller than our limit, then it is space between letter and do not divide it.
    maxChange = 0
    changePoint = None
    for i in range(len(points) - 1):
        diff = points[i + 1] - points[i]
        if diff > maxChange:
            maxChange = diff
            changePoint = (points[i], points[i + 1])
    return changePoint[0]

def findHorizontalCenterZeros(data: list[int]) -> list[int]:
    # it returns the indexes of zero that is in the center of zero sequence. 
    # We'll use it as a horizontal dividing point. For example :
    # [0, 0, 0, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 1, 2]
    # it will return [1, 10]
    # there are two 0 sequences and this returned list are the indexes of the center zeros in each sequence
    centerZeros = []
    startIndex = None
    for i, num in enumerate(data):
        if num == 0:
            if startIndex is None:
                startIndex = i
        else:
            if startIndex is not None:
                centerIndex = (startIndex + i - 1) // 2
                centerZeros.append(centerIndex)
                startIndex = None
    return centerZeros

def findVerticalCenterZeros(data: list[int], limit: int) -> list[int]:
    # same thing as findHorizontalCenterZeros(), but vertical version
    centerZeros = []
    startIndex = None
    for i, num in enumerate(data):
        if num == 0:
            if startIndex is None:
                startIndex = i
        else:
            if startIndex is not None:
                if i - startIndex > limit:
                    centerIndex = (startIndex + i - 1) // 2
                    centerZeros.append(centerIndex)
                startIndex = None
    return centerZeros

def perfectDividingPoints(data: list[int], imagePath: str) -> list[int]:
    # Our code first divide an image into the lines and then divide lines into the words.
    # If the lines are too close to each other, sometimes there is not a space between them and our traditional code does not divide to lines in these cases
    # So, we need a new approach to handle these problem
    # As, you can see in the first picture above, sometimes there is no spacings between lines (red parts show the spacings and it never down to zero)
    # Our code search for the zero pixel between lines and in the images like above it will not find this space and will not divide image into lines
    # perfectDividingPoints() function search for the point where the the number of pixels is minimum. It will use this point as a perfect dividing point
    # But what if there is minimum points more than one ? As you know dividing point should be unique for each line.
    # To prevent it, this function search for the minimum number and if there are two or more minimum number it take the one which is the nearest to the center
    # After find the number the minimum number which is the nearest to the center, we find its index in the all data and use it as a dividing point. (2nd image)

    def findSequences(data):
        # find the sequences where can be spacings between lines
        # I have used 200 for threshold. It means it take the sequences where the number of black pixels are smaller than 200
        result = []
        currentSequence = []
        for num in data:
            if num < 200:
                currentSequence.append(num)
            else:
                if currentSequence:
                    if len(currentSequence) > 3:
                        result.append(currentSequence)
                    currentSequence = []
        if currentSequence:
            result.append(currentSequence)
        return result

    def centerMinimum(sequence):
        # find the the index of the number in the sequence which is minimum and nearest the center
        centerIndex = len(sequence) // 2
        minIndexes = [i for i, v in enumerate(sequence) if v == min(sequence)]
        return min(minIndexes, key=lambda num: abs(num - centerIndex))

    def findSequencePosition(data, sequence):
        # I have divided the red parts that you see in the image into separate lists. 
        # So if we want to find the index of dividing point at the
        # whole data, we need to know where is the start point of our sublist in general list.
        for index in range(len(data)):
            foundSequence = data[index: index + len(sequence)]
            if foundSequence == sequence:
                return index
        return None

    # contains divided sequences from the whole sequence
    sequences = findSequences(data)
    # contains the dividing indexes
    indexes = []
    for sequence in sequences:
        pos = findSequencePosition(data, sequence)
        if pos is not None:
            indexes.append(pos + centerMinimum(sequence))

    image = Image.open(imagePath)
    _, height = image.size

    difference = height - len(data)
    return [x + difference for x in indexes]