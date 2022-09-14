import os
import cv2
from core.utils import read_class_names
from core.config import cfg
from tensorflow._api.v2.compat.v1 import ConfigProto
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from tensorflow._api.v2.compat.v1 import InteractiveSession

input_size = 416
padding = 5
weights='./localisation/checkpoints/yolov4-416'

def load_model():
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    #session = InteractiveSession(config=config)
    # load model
    saved_model_loaded = tf.saved_model.load(weights, tags=[tag_constants.SERVING])
    return saved_model_loaded

# function for cropping each detection and saving as new image
def crop_objects(img, data, path, allowed_classes, img_name):
    boxes, scores, classes, num_objects = data
    print(img_name + ":" + str(num_objects))
    if num_objects == 0:
        img_path = os.path.join(str(os.getcwd), "localisation", "data", img_name)
        return False, img_path
    else:
        #class_names = read_class_names(cfg.YOLO.CLASSES)
        #create dictionary to hold count of objects for image name
        #counts = dict()
        #for i in range(num_objects):
        # get count of class for part of image name
        print("detected")
        # get box coords
        xmin, ymin, xmax, ymax = boxes[0]
        # crop detection from image (take an additional 5 pixels around all edges)
        """if xmin < padding or xmax > (input_size - padding) or ymin < padding or ymax > (input_size - padding):
            cropped_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]
        else:
            cropped_img = img[int(ymin) - padding : int(ymax) + padding, int(xmin) - padding : int(ymax) + padding]"""
        cropped_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]
        # construct image name and join it to path for saving crop properly
        #if counter == 1:
        image_name = img_name + '.png'
        # else:
        #     image_name = img_name + "_" + str(counter) + ".png"
        #counter += 1
        img_path = os.path.join(path, image_name)
        # save image
        cv2.imwrite(img_path, cropped_img)
        return True, img_path