import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

#merges overlapping contours into one character
def mergecontours(imageResult, thresh, minX, minY, maxX, maxY, im2):
    charCopy = np.zeros((44, 24))
    # draw the rectangle
    char = thresh[minY - 35:maxY + 35, minX - 5:maxX + 5]
    char = cv2.resize(char, (20, 40))
    
    cv2.rectangle(im2, (minX - 5, minY - 40), (maxX + 5, maxY + 40), (0, 255, 0), 2)
    char = cv2.bitwise_not(char)

    charCopy[2:42, 2:22] = char
    charCopy[0:2, :] = 0
    charCopy[:, 0:2] = 0
    charCopy[42:44, :] = 0
    charCopy[:, 22:24] = 0
    imageResult.append(charCopy)

def segmentCharacters(path):

    #preprocessing on original image to be ready to get all contours
    gray = cv2.imread(path, 0)
    gray = cv2.resize(gray, (200, 100))
    gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilation = cv2.dilate(thresh, rect_kern, iterations=1)
    # cv2.imshow("", dilation)

    # find all contours
    try:
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    except:
        ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERAL, cv2.CHAIN_APPROX_SIMPLE)
    #sort largest 10 contours by area
    Contourss = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    # create copy of image
    im2 = gray.copy()
    imageResult = []  #list that carries segmented characters to be sent to recognition model
    listOfContours = []  #list that carries x coordinates of each contour to help ordering them (from left to right)

    #dictionary of key:contour number and value :list of cooridinates of this contour
    #helps in detecting overlapping contours
    contourDictionary = {}
    contourCoordinates = []
    contourNumber = -1

    # loop through all contours and filter them to find the required characters

    for cnt in Contourss:
        x, y, w, h = cv2.boundingRect(cnt)
        height, width = im2.shape
        # if height of contour is less than 50 pixels then filter it
        if float(h) < 50:
            continue
        ratio = h / float(w)
        area = h * w
        # if width of contour is more than 90 pixels then filter it
        if float(w) > 90:
            continue
        # if area of contour is less than 1000 pixels then filter it
        if area < 1000:
            continue
        # if ratio between contour's height and width is more than 7.5 then filter it
        if ratio > 7.5:
            continue
        # if x coordinate of contour located in first 11 pixels then skip it
        # if x < 12:
        #     continue
        # if x coordinate of contour located in last 35 pixels then skip it
        if x > 565:
            continue
        # if y coordinate of contour located in first 75 pixels then skip it
        if y < 75:
            continue
        listOfContours.append(x)

        #fill contourDictionary
        xmax = x + w
        ymax = y + h
        contourNumber += 1
        contourCoordinates = [x, y, xmax, ymax]
        contourDictionary[contourNumber] = contourCoordinates

        charCopy = np.zeros((44, 24))
        # draw the rectangle surrounding the contour
        char = thresh[y - 35:y + h + 35, x - 5:x + w + 5]

        #crop characters into small images to be sent to recognition model
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

    # overlapping contours detection

    todelete = []#list to delete contours replaced by new generated contour
    for ii in contourDictionary:
        for jj in contourDictionary:

            # dimensions of intersecting part between overlapping contours
            maxYintersect = min(contourDictionary[jj][3], contourDictionary[ii][3])
            minYintersect = max(contourDictionary[jj][1], contourDictionary[ii][1])
            maxXintersect = min(contourDictionary[jj][2], contourDictionary[ii][2])
            minXintersect = max(contourDictionary[jj][0], contourDictionary[ii][0])
            overlaparea = ((maxXintersect + 5) - (minXintersect - 5)) * ((maxYintersect + 35) - (minYintersect - 35))

            # dimensions of new generated contour from the two overlapping contours
            maxYmerge = max(contourDictionary[jj][3], contourDictionary[ii][3])
            minYmerge = min(contourDictionary[jj][1], contourDictionary[ii][1])
            maxXmerge = max(contourDictionary[jj][2], contourDictionary[ii][2])
            minXmerge = min(contourDictionary[jj][0], contourDictionary[ii][0])

            if ii == jj: # avoid comparing a contour with itself
                continue
            # overlap detection
            if contourDictionary[jj][3] + 35 > contourDictionary[ii][1] - 35 and \
                    contourDictionary[ii][3] + 35 > contourDictionary[jj][1] - 35:
                if contourDictionary[jj][2] + 5 > contourDictionary[ii][0] - 5 and \
                        contourDictionary[ii][2] + 5 > contourDictionary[jj][0] - 5:
                    if contourDictionary[ii][0] == contourDictionary[jj][0]:
                        contourDictionary[jj][0] += 1
                    if contourDictionary[ii][0] - contourDictionary[jj][0] > 0:
                        if overlaparea > 1500:# if area of intersction is less than 1500 ,so it's most likely they're
                            # different characters with overlapping contours, so we don't merge them

                            # merge the two overlappng contours into one big contour
                            mergecontours(imageResult, thresh, minXmerge, minYmerge, maxXmerge, maxYmerge, im2)

                            #add new generated contour's x coordinate to be put in it's right order
                            listOfContours.append(minXmerge)
                            # add overlapping contours to a list to be deleted
                            todelete.append(ii)
                            todelete.append(jj)

    # sort list of merged contours reversly to be deleted right without conflicts
    todelete.sort(reverse=True)

    for deletee in todelete:
        del listOfContours[deletee]
        del imageResult[deletee]

    indices = sorted(range(len(listOfContours)), key=lambda k: listOfContours[k])
    imageResultCopy = []

    for index in indices:
        if index < len(imageResult):
            imageResultCopy.append(imageResult[index])  # stores character images according to their index

    imageResult = np.array(imageResultCopy)
    imageResultCopy.clear()
    #return list of cropped characters images to be recognized in recognition model
    return imageResult
