from collections import namedtuple
from skimage.filters import threshold_local
from skimage import segmentation
from skimage import measure
from imutils import perspective
import numpy as np
import imutils
import cv2 as cv

# Main class which responsible for integration of whole image processing piplines
if __name__ == "__main__":
    print("main")
