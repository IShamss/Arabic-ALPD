import imp
import os

from matplotlib import pyplot as plt
from recognition.rec import Recognition
from recognition.KNN import classify_unlabelled_directory
from recognition.KNN import predictChars
from NewSegmentation.newSeg import segmentChars
from integeration.client import endPoint
from testing.webcam import stream
from NewSegmentation.oldSeg import Segmentation
# from integeration.merge import endPoint
from skimage.filters import threshold_local
from skimage import segmentation
from skimage import measure
from imutils import perspective
import numpy as np
import imutils
import cv2 as cv
import sys

path = './outputs/'
url = "http://192.168.1.103:8080/video"
sys.path.insert(0, './localisation')
import detect as detect
# from segmentation.seg import Segmentation
from absl import app


def predict(image_path):
    # crop_path = detect.crop_multiple(image_path)[0]
    detect.crop_one(image_path)[0]


def printChars(chars, count):
    if not os.path.isdir(f'{path}{count}'):
        os.makedirs(f'{path}{count}')

    for i in range(len(chars)):
        plt.subplot(1, 10, i + 1)
        plt.imshow(chars[i], cmap='gray')
        cv.imwrite(f'{path}{count}/{i + 1}.png', chars[i])
        plt.axis('off')
    # plt.show()


# Main  which responsible for integration of whole image processing pipelines
if __name__ == '__main__':
    try:
        countPlate = 1
        # stream(url)

        # localization
        detect.crop_multiple("./localisation/data/demo")[0]

        for filename in os.scandir("./detections/"):
            try:
                # segmentation
                _, chars = segmentChars(filename.path)

                # print chars segmented
                printChars(chars, countPlate)

                # recognition
                predicted_chars = classify_unlabelled_directory(f'{path}{countPlate}/')

                # print string
                lp = predictChars(predicted_chars)
                print(lp)

                os.rmdir(f'./outputs/{countPlate}')
                countPlate += 1

                # send string to middle-ware
                endPoint(lp)

            except Exception:
                # print("error")
                continue

    except SystemExit:
        pass

# segObject = Segmentation(filename.path)
# chars = segObject.run()
# segObject = Segmentation(filename.path)
# len1, chars1 = segmentChars(filename.path)
# len2, chars2 = segObject.run()
# mx = max(len1, len2)
# chars = chars1
# if mx == len1 and len1 <= 7:
#     print("================== First ===================")
# else:
#     print("================== Second ===================")
#     chars = chars2
