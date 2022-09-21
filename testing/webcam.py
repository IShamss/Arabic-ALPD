import glob

import cv2 as cv
import os

path = './localisation/data/images/1.png'


def stream(link):
    # link of streaming
    # link = "http://9.246.91.33:8080/video"
    capture = cv.VideoCapture(link)
    files = glob.glob('./localisation/data/images/*')
    for file in files:
        os.remove(file)
    while True:

        _, frame = capture.read()
        img = cv.resize(frame, (500, 500))
        cv.imshow('livestream', img)

        # take photo from streaming
        if cv.waitKey(1) == ord("q"):
            cv.imwrite(path, frame)
            break

        #     # exit streaming
        # if cv.waitKey(1) == ord('z'):
        #     break

    # destroy streaming
    capture.release()
    cv.destroyAllWindows()
# ds

# stream()
