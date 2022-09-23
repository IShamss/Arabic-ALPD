import os
import sys

# from integeration.merge import endPoint
import cv2 as cv
from matplotlib import pyplot as plt

from NewSegmentation.newSeg import segmentChars
from recognition.KNN import classify_unlabelled_directory
from recognition.KNN import predictChars

path = './outputs/'
url = "http://192.168.98.146:8080/video"
sys.path.insert(0, './localisation')
import detect as detect


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
    while True:
        # try:
        countPlate = 1
        # stream(url)

        # localization
        detect.crop_multiple("./localisation/data/demo/", False)

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

                countPlate += 1

                # send string to middle-ware
                # endPoint(lp)
                # files = glob.glob('./detections/*')
                # for file in files:
                #     os.remove(file)
                # files = glob.glob('./outputs/1/*')
                # for file in files:
                #     os.remove(file)

            except Exception:
                print("error")
                continue

    # except Exception:
    #     print("outer error")
    #     continue

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
