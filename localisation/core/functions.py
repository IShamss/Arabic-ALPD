import os

import cv2
import tensorflow as tf
from tensorflow._api.v2.compat.v1 import ConfigProto
from tensorflow.python.saved_model import tag_constants

input_size = 416
padding = 5
weights = './localisation/checkpoints/yolov4-416'


def load_model():
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    # session = InteractiveSession(config=config)
    # load model
    saved_model_loaded = tf.saved_model.load(weights, tags=[tag_constants.SERVING])
    return saved_model_loaded


# function for cropping each detection and saving as new image
def crop_objects(img, data, path, img_name, detect_multiple):
    boxes, scores, classes, num_objects = data
    if num_objects == 0:
        img_path = os.path.join(str(os.getcwd), "localisation", "data", img_name)
        return False, img_path
    elif num_objects == 1 or not detect_multiple:
        # for i in range(num_objects):
        # get count of class for part of image name
        print("detected")
        # get box coords
        xmin, ymin, xmax, ymax = boxes[0]
        # crop detection from image
        cropped_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]
        # construct image name and join it to path for saving crop properly
        image_name = img_name + '.png'

        # counter += 1
        img_path = os.path.join(path, image_name)
        # save image
        cv2.imwrite(img_path, cropped_img)
        return True, img_path
    else:
        print("detected " + str(num_objects))
        counter = 1
        for i in range(num_objects):
            # get box coords
            xmin, ymin, xmax, ymax = boxes[i]
            # crop detection from image
            cropped_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]
            # construct image name and join it to path for saving crop properly
            if counter == 1:
                image_name = img_name + '.png'
            else:
                image_name = img_name + "_" + str(counter) + ".png"
            # counter += 1
            img_path = os.path.join(path, image_name)
            # save image
            cv2.imwrite(img_path, cropped_img)
        return True, img_path
