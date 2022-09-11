from collections import namedtuple
from skimage.filters import threshold_local
from skimage import segmentation
from skimage import measure
from imutils import perspective
import numpy as np
import imutils
import cv2 as cv
import sys
sys.path.insert(0, '../localisation')
import detect as detect
from absl import app
import core.common as common
import core.backbone as backbone
import core.config as cfg
import core.functions as func
import core.utils as utils
import core.yolov4 as yv4

# Main class which responsible for integration of whole image processing piplines
def predict(image_path):
    crop_path = detect.crop_one(image_path)[0]

def main(_argv):
    predict("../localisation/data/images/IMG_5351.JPEG")

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass