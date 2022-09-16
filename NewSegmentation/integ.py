import os
import cv2 as cv

path = './output/'
from matplotlib import pyplot as plt
from oldSeg import Segmentation
from newSeg import segmentChars


def printChars(chars, count):
    # if not os.path.isdir(f'{path}{count}'):
    #     os.makedirs(f'{path}{count}')
    for i in range(len(chars)):
        plt.subplot(1, 10, i + 1)
        plt.imshow(chars[i], cmap='gray')
        # cv.imwrite(f'{path}{count}.png', chars[i])
        count += 1
        plt.axis('off')
    plt.show()


if __name__ == "__main__":
    j = 1
    for filename in os.scandir("../facebook"):
        try:
            segObject = Segmentation(filename.path)
            len1, chars1 = segmentChars(filename.path)
            len2, chars2 = segObject.run()
            mx = max(len1, len2)
            chars = chars1
            if mx == len1 and len1 <= 7:
                print("================== First ===================")
            else:
                print("================== Second ===================")
                chars = chars2
            printChars(chars, j)
            j += len(chars)
        except Exception:
            print("============== Error ==============")
            continue
