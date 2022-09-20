import cv2 as cv

path = '../outputs/'


def stream():
    link = "http://192.168.1.103:8080/video"
    # link of streaming
    capture = cv.VideoCapture(link)
    while True:

        _, frame = capture.read()
        img = cv.resize(frame, (500, 500))
        cv.imshow('livestream', img)

        # take photo from streaming
        if cv.waitKey(1) == ord("q"):
            cv.imwrite(f'{path}1.png', frame)
            continue

            # exit streaming
        if cv.waitKey(1) == ord('z'):
            break

    # destroy streaming
    capture.release()
    cv.destroyAllWindows()
#ds

# stream()
