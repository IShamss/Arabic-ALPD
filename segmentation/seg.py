import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

class Segmentation:
    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.image = cv.imread(self.imagePath)
        self.listOfContours = []
        self.chars = []
        # print("Segmentation Constructor")

    def blurring(self):

        self.image = cv.GaussianBlur(self.image, (5, 5), cv.BORDER_DEFAULT)

    def thresholding(self):
        # Preprocess cropped license plate image
        self.image = cv.resize(self.image, (500, 300))
        img_gray_lp = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        _, self.image = cv.threshold(img_gray_lp, 150, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    def filtering(self):
        img_binary_lp = cv.erode(self.image, (3, 3))
        self.image = cv.dilate(img_binary_lp, (3, 3))

    def findContours(self, dimensions):

        # Find all contours in the image
        _,contours, _ = cv.findContours(self.image.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Retrieve potential dimensions
        lowerWidth = dimensions[0]
        upperWidth = dimensions[1]
        lowerHeight = dimensions[2]
        upperHeight = dimensions[3]

        # Check largest 10 contours for license plate or character
        contours = sorted(contours, key=cv.contourArea, reverse=True)[:10]
        copyImage = self.image
        imageResult = []

        for contour in contours:
            # detects contour in binary image and returns the coordinates of surrounding rectangle
            intX, intY, intWidth, intHeight = cv.boundingRect(contour)

            # checking the dimensions of the contour to filter characters by contour's size
            if intWidth > lowerWidth and intWidth < upperWidth and intHeight > lowerHeight and intHeight < upperHeight:
                self.listOfContours.append(
                    intX)  # stores the x coordinate of the character's contour, to used later for indexing the contours

                charCopy = np.zeros((44, 24))
                # extracting each character using the surrounding rectangle's coordinates.
                char = self.image[intY - 25:intY + intHeight + 25, intX:intX + intWidth]
                char = cv.resize(char, (20, 40))

                cv.rectangle(copyImage, (intX, intY - 25), (intWidth + intX, intHeight + intY + 25), (50, 21, 200), 2)

                # Resize the image to 24x44 with black border
                charCopy[2:42, 2:22] = char
                charCopy[0:2, :] = 0
                charCopy[:, 0:2] = 0
                charCopy[42:44, :] = 0
                charCopy[:, 22:24] = 0

                imageResult.append(charCopy)  # List that stores the character's binary image (unsorted)
        # Return characters on ascending order with respect to the x-coordinate (most-left character first)

        # arbitrary function that stores sorted list of character indeces
        indices = sorted(range(len(self.listOfContours)), key=lambda k: self.listOfContours[k])
        imageResultCopy = []

        for index in indices:
            imageResultCopy.append(imageResult[index])  # stores character images according to their index
        imageResult = np.array(imageResultCopy)

        # Get contours within cropped license plate
        return imageResult

    def segmentCharacters(self):

        LP_WIDTH = self.image.shape[0]
        LP_HEIGHT = self.image.shape[1]

        # Make borders white
        self.image[0:4, :] = 255
        self.image[:, 0:4] = 255
        self.image[65:75, :] = 255
        self.image[:, 330:333] = 255

        # Estimations of character contours sizes of cropped license plates
        dimensions = [LP_WIDTH / 20, LP_WIDTH / 2, LP_HEIGHT / 15, 2 * LP_HEIGHT / 3]
        return dimensions

    def run(self):
        # self.GaussianBlur()
        self.thresholding()
        self.filtering()
        dimensions=self.segmentCharacters()
        return self.findContours(dimensions)


# segObj=Segmentation(r"C:\Users\ZZ01GX865\Desktop\CV\TestCases\20220906_131817.png")
# char=segObj.run()
# for i in range(len(segObj.listOfContours)):
#     plt.subplot(1, 10, i + 1)
#     plt.imshow(char[i], cmap='gray')
#     plt.axis('off')
# plt.show()