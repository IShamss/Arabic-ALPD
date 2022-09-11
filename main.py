import os
from collections import namedtuple

from matplotlib import pyplot as plt
from skimage.filters import threshold_local
from skimage import segmentation
from skimage import measure
from imutils import perspective
import numpy as np
import imutils
import cv2 as cv
import sys

path = 'C:/Alpd/alpd/outputs/'
sys.path.insert(0, '../localisation')
import detect as detect
from segmentation.seg import Segmentation
from absl import app


# import core.common as common
# import core.backbone as backbone
# import core.config as cfg
# import core.functions as func
# import core.utils as utils
# import core.yolov4 as yv4

# Main class which responsible for integration of whole image processing piplines
def predict(image_path):
    crop_path = detect.crop_one(image_path)[0]


def main(_argv):
    predict("../localisation/data/images/IMG_5351.JPEG")


def printChars(chars, segObj, count):
    if not os.path.isdir(f'{path}{count}'):
        os.makedirs(f'{path}{count}')
    for i in range(len(segObj.listOfContours)):
        plt.subplot(1, 10, i + 1)
        plt.imshow(chars[i], cmap='gray')
        cv.imwrite(f'{path}{count}/{i + 1}.png', chars[i])
        plt.axis('off')


if __name__ == '__main__':
    try:
        # app.run(main)
        countPlate = 1
        for filename in os.scandir("testcases"):
            segObject = Segmentation(filename.path)
            chars = segObject.run()
            printChars(chars, segObject, countPlate)
            countPlate += 1

    except SystemExit:
        pass
