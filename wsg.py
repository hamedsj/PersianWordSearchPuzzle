import cv2
import numpy as np
import random


class point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class direction:
    diagonal_down_right = "diagonal_down_right"
    diagonal_up_right = "diagonal_up_right"
    diagonal_up_left = "diagonal_up_left"
    diagonal_down_left = "diagonal_down_left"
    horizontal_left = "horizontal_left"
    horizontal_right = "horizontal_right"
    vertical_up = "vertical_up"
    vertical_down = "vertical_down"


fa_abc = ['ا', "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ",
          "ف", "ق", "ک", "گ", "ل", "م", "ن", "و", "ه", "ی"]

grid = 10

table = []

used_points = []

words = []


def addAlphaChannelToImage(img):
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    img_bgra = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    return img_bgra


def init_table():
    for i in range(grid * grid):
        table.append(fa_abc[random.randint(0, 31)])


def checkCoordinatesInGrid(x: int, y: int):
    if x < 0 or y < 0:
        return False
    if x >= grid or y >= grid:
        return False
    return True


def printTable():
    for i in range(grid):
        for j in range(grid):
            print("\t" + table[i * grid + j], end="")
        if i != grid - 1:
            print("\n")


def getImageOfRow(row: int):
    res = cv2.imread("alphabet/a" + str(fa_abc.index(table[row * grid]) + 1) + ".png", cv2.IMREAD_UNCHANGED)
    for i in range(grid - 1):
        img = cv2.imread("alphabet/a" + str(fa_abc.index(table[row * grid + i + 1]) + 1) + ".png", cv2.IMREAD_UNCHANGED)
        res = np.hstack((res, img))
    return res


def writeTableImage(path):
    try:
        output = getImageOfRow(0)
        for i in range(grid - 1):
            img = getImageOfRow(i + 1)
            output = np.vstack((output, img))
        bg = cv2.imread("bg.jpg", cv2.IMREAD_UNCHANGED)
        w, h, c = output.shape
        bg = cv2.resize(bg, (w, h))
        bg = addAlphaChannelToImage(bg)
        cv2.imwrite(path, cv2.add(bg, output))
    except Exception as e:
        print("\n" + str(e))


def checkCoordinatesIsUsed(x: int, y: int, word: str):
    for p in used_points:
        if p.x == x and p.y == y and table[p.y * grid + p.x] != word[0]:
            return True
    return False


def is_empty_together(p: point, length: int, word=""):
    if checkCoordinatesIsUsed(p.x, p.y, word[0]):
        return "no"

    tempX = p.x
    tempY = p.y
    diagonal_down_right = False
    for i in range(length - 1):
        tempX += 1
        tempY += 1
        if not checkCoordinatesInGrid(tempX, tempY):
            diagonal_down_right = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            diagonal_down_right = False
            break
        if i == length - 2:
            diagonal_down_right = True
    if diagonal_down_right:
        return direction.diagonal_down_right

    tempX = p.x
    tempY = p.y
    diagonal_up_right = False
    for i in range(length - 1):
        tempX += 1
        tempY -= 1
        if not checkCoordinatesInGrid(tempX, tempY):
            diagonal_up_right = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            diagonal_up_right = False
            break
        if i == length - 2:
            diagonal_up_right = True
    if diagonal_up_right:
        return direction.diagonal_up_right

    tempX = p.x
    tempY = p.y
    diagonal_up_left = False
    for i in range(length - 1):
        tempX -= 1
        tempY -= 1
        if not checkCoordinatesInGrid(tempX, tempY):
            diagonal_up_left = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            diagonal_up_left = False
            break
        if i == length - 2:
            diagonal_up_left = True
    if diagonal_up_left:
        return direction.diagonal_up_left

    tempX = p.x
    tempY = p.y
    diagonal_down_left = False
    for i in range(length - 1):
        tempX -= 1
        tempY += 1
        if not checkCoordinatesInGrid(tempX, tempY):
            diagonal_down_left = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            diagonal_down_left = False
            break
        if i == length - 2:
            diagonal_down_left = True
    if diagonal_down_left:
        return direction.diagonal_down_left

    tempX = p.x
    tempY = p.y
    horizontal_left = False
    for i in range(length - 1):
        tempX -= 1
        if not checkCoordinatesInGrid(tempX, tempY):
            horizontal_left = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            horizontal_left = False
            break
        if i == length - 2:
            horizontal_left = True
    if horizontal_left:
        return direction.horizontal_left

    tempX = p.x
    tempY = p.y
    horizontal_right = False
    for i in range(length - 1):
        tempX += 1
        if not checkCoordinatesInGrid(tempX, tempY):
            horizontal_right = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            horizontal_right = False
            break
        if i == length - 2:
            horizontal_right = True
    if horizontal_right:
        return direction.horizontal_right

    tempX = p.x
    tempY = p.y
    vertical_up = False
    for i in range(length - 1):
        tempY -= 1
        if not checkCoordinatesInGrid(tempX, tempY):
            vertical_up = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            vertical_up = False
            break
        if i == length - 2:
            vertical_up = True
    if vertical_up:
        return direction.vertical_up

    tempX = p.x
    tempY = p.y
    vertical_down = False
    for i in range(length - 1):
        tempY += 1
        if not checkCoordinatesInGrid(tempX, tempY):
            vertical_down = False
            break
        if checkCoordinatesIsUsed(tempX, tempY, word[i + 1]):
            vertical_down = False
            break
        if i == length - 2:
            vertical_down = True
    if vertical_down:
        return direction.vertical_down

    return "no"


def add_word_to_coordinates(word: str, x: int, y: int, way: str):
    for i in range(word.__len__()):
        table[y * grid + x] = word[i]
        used_points.append(point(x=x, y=y))
        if way == direction.vertical_down:
            y += 1
        elif way == direction.vertical_up:
            y -= 1
        elif way == direction.horizontal_right:
            x += 1
        elif way == direction.horizontal_left:
            x -= 1
        elif way == direction.diagonal_down_left:
            y += 1
            x -= 1
        elif way == direction.diagonal_up_left:
            y -= 1
            x -= 1
        elif way == direction.diagonal_up_right:
            y -= 1
            x += 1
        elif way == direction.diagonal_down_right:
            y += 1
            x += 1


def add_word_to_table(word: str):
    firstX = random.randint(0, grid - 1)
    firstY = random.randint(0, grid - 1)
    end_iterate = False
    first_end = False
    while True:
        p = point(firstX, firstY)
        way = is_empty_together(p, word.__len__(), word)
        if way != "no":
            add_word_to_coordinates(word=word, x=p.x, y=p.y, way=way)
            break
        else:
            if firstX >= grid - 1:
                if firstY >= grid - 1 and end_iterate and first_end:
                    reset()
                    break
                firstX = 0
                firstY += 1
                if firstY >= grid - 1 and not first_end:
                    first_end = True
                    end_iterate = True
            else:
                firstX += 1


def reset():
    try:
        global table
        global used_points
        table = []
        used_points = []
        init_table()
        for word in words:
            add_word_to_table(word)
    except:
        reset()


def main(path: str, size: int, words1):
    global grid
    global words
    grid = size
    words = words1
    try:
        init_table()
        for word in words1:
            add_word_to_table(word)
        printTable()
        writeTableImage(path)
    except Exception as e:
        reset()


if __name__ == "__main__":
    size = int(input("enter puzzle size : "))
    words = []
    word = input("enter a word : ")
    words.append(word)
    while word != int(-1):
        word = input("enter a word : ")
        if word == -1:
            break
        words.append(word)
    main(path="output.png", size=size, words1=words)
