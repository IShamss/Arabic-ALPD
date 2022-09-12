from distutils.log import error
import os
from collections import namedtuple

from matplotlib import pyplot as plt
from recognition.rec import Recognition

from skimage.filters import threshold_local
from skimage import segmentation
from skimage import measure
from imutils import perspective
import numpy as np
import imutils
import cv2 as cv
import sys

path = './outputs/'
sys.path.insert(0, './localisation')
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



#def main(_argv):
 #   predict("./localisation/data/images/IMG_5351.JPEG")


def printChars(chars, segObj, count):
    if not os.path.isdir(f'{path}{count}'):
        os.makedirs(f'{path}{count}')
    for i in range(len(segObj.listOfContours)):
        plt.subplot(1, 10, i + 1)
        plt.imshow(chars[i], cmap='gray')
        cv.imwrite(f'{path}{count}/{i + 1}.png', chars[i])
        plt.axis('off')
    plt.show()

if __name__ == '__main__':
    try:
        # app.run(main)
        countPlate = 1
        predict("./localisation/data/images/IMG_5482.JPEG")
        rec = Recognition('vgg_model')
        for filename in os.scandir(".\detections"):
            try:
                segObject = Segmentation(filename.path)
                chars = segObject.run()
                printChars(chars, segObject, countPlate)
                countPlate += 1
            except Exception:
                print("error")
                continue
        for filename in os.scandir("./outputs/1"):
            rec.test_data([filename.path])
            #rec.test_data(['./outputs/1/1.png', './outputs/1/2.png',
            #            './outputs/1/3.png', './outputs/1/4.png', './outputs/1/5.png', './outputs/1/6.png'])
    except SystemExit:
        pass
