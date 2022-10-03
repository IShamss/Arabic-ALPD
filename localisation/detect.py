import os
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import flags
import core.utils as utils
from core.functions import *
import cv2
import numpy as np

flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './localisation/checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_list('images', './localisation/data/images/car3.jpg', 'path to input image')
flags.DEFINE_string('output', './localisation/detections/', 'path to output folder')
flags.DEFINE_boolean('count', False, 'count objects within images')
flags.DEFINE_boolean('dont_show', False, 'dont show image output')
flags.DEFINE_boolean('info', False, 'print info on detections')
flags.DEFINE_boolean('crop', True, 'crop detections from images')
flags.DEFINE_boolean('ocr', False, 'perform generic OCR on detection regions')
flags.DEFINE_boolean('plate', False, 'perform license plate recognition')

weights = './localisation/checkpoints/yolov4-416'
iou = 0.45
score = 0.50
size = 416
image_extensions = (".jpg", ".JPG", ".png", ".PNG", ".jpeg", ".JPEG")


def detect_and_crop(image_path, saved_model_loaded, detect_multiple):
    # loop through images in list and run Yolov4 model on each
    original_image_clrs = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image_clrs, cv2.COLOR_BGR2RGB)

    image_data = cv2.resize(original_image, (size, size))
    image_data = image_data / 255.

    # get image name by using split method
    image_name_ext = image_path.split('/')[-1]
    image_name = image_name_ext.split('.')[0]

    images_data = []
    for i in range(1):
        images_data.append(image_data)
    images_data = np.asarray(images_data).astype(np.float32)

    infer = saved_model_loaded.signatures['serving_default']
    batch_data = tf.constant(images_data)
    pred_bbox = infer(batch_data)
    for key, value in pred_bbox.items():
        boxes = value[:, :, 0:4]
        pred_conf = value[:, :, 4:]

    # run non max suppression on detections
    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape(
            pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        iou_threshold=iou,
        score_threshold=score
    )

    # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
    original_h, original_w, _ = original_image.shape
    bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)

    for bbox in bboxes:
        if bbox[0] != 0 and bbox[1] != 0 and bbox[2] != 0 and bbox[3] != 0:
            cv2.rectangle(original_image_clrs, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0),
                          12)

    img_path = "./green_boxes"
    try:
        os.mkdir(img_path)
    except FileExistsError:
        pass

    img_path = img_path + "/" + image_name_ext
    cv2.imwrite(img_path, original_image_clrs)

    # hold all detection data in one variable
    pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]

    # read in all class names from config
    # class_names = utils.read_class_names(cfg.YOLO.CLASSES)

    # by default allow all classes in .names file
    # allowed_classes = list(class_names.values())

    # if crop flag is enabled, crop each detection and save it as new image
    crop_path = os.path.join(os.getcwd(), 'detections')
    try:
        os.mkdir(crop_path)
    except FileExistsError:
        pass
    detected, crop_path = crop_objects(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), pred_bbox, crop_path,
                                       image_name, detect_multiple=False)

    if detected:
        crop_path = os.path.relpath(crop_path, start=os.curdir)
        crop_path.replace(os.sep, '/')
        return crop_path
    else:
        print("No license plate detected")
        return None


def crop_one(image_path, detect_multiple, saved_model_loaded):
    # saved_model_loaded = load_model()
    crop_path = detect_and_crop(image_path, saved_model_loaded, detect_multiple)
    if crop_path is not None:
        return crop_path


def crop_multiple(directory_path, detect_multiple=False, saved_model_loaded=False):
    #saved_model_loaded = load_model()
    final_crop_paths = []
    not_detected = []
    image_paths = []
    file_paths = os.listdir(directory_path)
    image_paths = [(os.path.join(directory_path, path)).replace(os.sep, '/') for path in file_paths if path.endswith(image_extensions)]
    # final_crop_paths = [detect_and_crop(image_path, saved_model_loaded, detect_multiple) for image_path in image_paths]
    for image in image_paths:
        crop_path = detect_and_crop(image, saved_model_loaded, detect_multiple)
        if crop_path is not None:
            final_crop_paths.append(crop_path)
    return final_crop_paths


if __name__ == '__main__':
    try:
        # crop_one("./localisation/data/images/IMG (185).jpeg")
        crop_multiple("./localisation/data/images")
    except SystemExit:
        pass
