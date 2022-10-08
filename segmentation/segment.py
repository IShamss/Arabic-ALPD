path = './output/'
j = 1
import cv2
import numpy as np


def segmentChars(filename):
    # for filename in os.scandir(longPath):
    gray = cv2.imread(filename, 0)
    gray = cv2.resize(gray, (200, 100))
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.medianBlur(gray, 3)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    # cv2.imshow("Otsu", thresh)
    # cv2.waitKey(0)
    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # apply dilation
    dilation = cv2.dilate(thresh, rect_kern, iterations=1)
    # find contours
    try:
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Contourss = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    # create copy of image
    im2 = gray.copy()
    plate_num = ""
    imageResult = []
    listOfContours = []
    # loop through contours and find letters in license plate
    for cnt in Contourss:
        x, y, w, h = cv2.boundingRect(cnt)
        height, width = im2.shape
        # if height of box is not a quarter of total height then skip
        if float(h) < height / 8:
            continue
        ratio = h / float(w)
        # if height to width ratio is less than 1.5 skip
        area = h * w
        # if width is not more than 25 pixels skip
        if float(w) > width / 7:
            continue
        # if area is less than 100 pixels skip
        if area < 1000:
            continue
        if ratio > 7.5:
            continue
        listOfContours.append(x)
        # print(len(listOfContours))

        charCopy = np.zeros((44, 24))
        # draw the rectangle
        # char = thresh[y - 5:y + h + 5, x - 5:x + w + 5]
        char = thresh[y - 35:y + h + 35, x - 5:x + w + 5]
        try:
            char = cv2.resize(char, (20, 40))
        except Exception:
            continue

        cv2.rectangle(im2, (x - 5, y - 40), (x + w + 5, y + h + 18), (0, 255, 0), 2)
        char = cv2.bitwise_not(char)
        # roi = cv2.medianBlur(roi,5)
        #     # cv2.imshow("ROI", roi)
        charCopy[2:42, 2:22] = char
        charCopy[0:2, :] = 0
        charCopy[:, 0:2] = 0
        charCopy[42:44, :] = 0
        charCopy[:, 22:24] = 0
        imageResult.append(charCopy)
    indices = sorted(range(len(listOfContours)), key=lambda k: listOfContours[k])
    imageResultCopy = []
    # print(len(imageResult))
    # print(len(indices))
    for index in indices:
        if index < len(imageResult):
            imageResultCopy.append(imageResult[index])  # stores character images according to their index
    imageResult = np.array(imageResultCopy)
    # cv2.imshow("Character's Segmented", im2)
    return len(indices), imageResult
    # imageResultCopy.clear()
    # print(len(listOfContours))
    # for i in range(len(imageResult)):
    #     plt.subplot(1, 10, i + 1)
    #     # plt.imshow(imageResult[i], cmap='gray')
    #     cv2.imwrite(f'{path}{j}.png', imageResult[i])
    #     j += 1
    #     plt.axis('off')
    # # plt.show()
    # cv2.imshow("Character's Segmented", im2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def newOldSegmentation(filename):
    gray = cv2.imread(filename, 0)
    gray = cv2.resize(gray, (200, 100))
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # gray = cv2.medianBlur(gray, 3)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # apply dilation
    dilation = cv2.dilate(thresh, rect_kern, iterations=1)
    # kernel = np.ones((3, 3), np.uint8)
    # dilation = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # dilation = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

    # cv2.imshow("", dilation)
    # find contours
    try:
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERAL, cv2.CHAIN_APPROX_SIMPLE)
    Contourss = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    # create copy of image
    im2 = gray.copy()
    plate_num = ""
    imageResult = []
    listOfContours = []
    # loop through contours and find letters in license plate

    for cnt in Contourss:
        x, y, w, h = cv2.boundingRect(cnt)
        height, width = im2.shape
        # if height of box is not a quarter of total height then skip
        if float(h) < 50:
            continue
        ratio = h / float(w)
        # if height to width ratio is less than 1.5 skip
        area = h * w
        # if width is not more than 25 pixels skip
        if float(w) > 90:
            continue
        # if area is less than 1000 pixels skip
        if area < 1000:
            continue
        if ratio > 7.5:
            continue
        if x < 12:
            continue
        if x > 565:
            continue
        if y < 75:
            continue
        listOfContours.append(x)

        # print(len(listOfContours))
        # print("      x:", x, "     y:", y, "     area:", area, "     width", w, "     height", h)
        # averagex+=x
        # averagey+=y

        charCopy = np.zeros((44, 24))
        # draw the rectangle
        char = thresh[y - 35:y + h + 35, x - 5:x + w + 5]
        try:
            char = cv2.resize(char, (20, 40))
        except Exception:
            continue

        cv2.rectangle(im2, (x - 5, y - 40), (x + w + 5, y + h + 40), (0, 255, 0), 2)
        char = cv2.bitwise_not(char)

        charCopy[2:42, 2:22] = char
        charCopy[0:2, :] = 0
        charCopy[:, 0:2] = 0
        charCopy[42:44, :] = 0
        charCopy[:, 22:24] = 0
        imageResult.append(charCopy)

    indices = sorted(range(len(listOfContours)), key=lambda k: listOfContours[k])
    imageResultCopy = []
    # print(len(imageResult))
    # print(len(indices))
    for index in indices:
        if index < len(imageResult):
            imageResultCopy.append(imageResult[index])  # stores character images according to their index

    imageResult = np.array(imageResultCopy)
    imageResultCopy.clear()
    return imageResult
