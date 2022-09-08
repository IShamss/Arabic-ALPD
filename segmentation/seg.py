import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage.filters import threshold_otsu
from PIL import Image
import os


# matplotlib widget
class Segmentation:
    def __init__(self, LocalizedImagePath):
        self.ImagePath = LocalizedImagePath
        print("Segmentation Constructor")



    def GaussianBlur(self):
        image = cv.imread(self.ImagePath)
        blurred = cv.GaussianBlur(image, (5, 5), cv.BORDER_DEFAULT)
        cv.imwrite(self.ImagePath, blurred)

    def Adaptive_Threshold(self):
        image = cv.imread(self.ImagePath)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        threshed = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 199, 5)
        cv.imwrite(self.ImagePath, threshed)

    def Masking(self):
        import os
        x_cntr_list = []
        img = cv.imread(self.ImagePath)
        arrOfChars = []

        def find_contours(dimensions, img):

            # Find all contours in the image
            cntrs, _ = cv.findContours(img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            # print(cntrs)

            # Retrieve potential dimensions
            lower_width = dimensions[0]
            upper_width = dimensions[1]
            lower_height = dimensions[2]
            upper_height = dimensions[3]

            # Check largest 5 or  15 contours for license plate or character respectively
            cntrs = sorted(cntrs, key=cv.contourArea, reverse=True)[:10]

            # ii = cv.imread('images/plate.jpg')
            ii = img

            target_contours = []
            img_res = []
            for cntr in cntrs:
                # detects contour in binary image and returns the coordinates of rectangle enclosing it
                intX, intY, intWidth, intHeight = cv.boundingRect(cntr)

                # checking the dimensions of the contour to filter out the characters by contour's size
                if intWidth > lower_width and intWidth < upper_width and intHeight > lower_height and intHeight < upper_height:
                    x_cntr_list.append(
                        intX)  # stores the x coordinate of the character's contour, to used later for indexing the contours

                    char_copy = np.zeros((44, 24))
                    # extracting each character using the enclosing rectangle's coordinates.
                    char = img[intY - 25:intY + intHeight + 25, intX:intX + intWidth]
                    char = cv.resize(char, (20, 40))

                    cv.rectangle(ii, (intX, intY - 25), (intWidth + intX, intHeight + intY + 25), (50, 21, 200), 2)
                    plt.imshow(ii, cmap='gray')

                    # Make result formatted for classification: invert colors
                    char = cv.subtract(255, char)

                    # Resize the image to 24x44 with black border
                    char_copy[2:42, 2:22] = char
                    char_copy[0:2, :] = 0
                    char_copy[:, 0:2] = 0
                    char_copy[42:44, :] = 0
                    char_copy[:, 22:24] = 0

                    img_res.append(char_copy)  # List that stores the character's binary image (unsorted)
            # Return characters on ascending order with respect to the x-coordinate (most-left character first)

            plt.show()
            # arbitrary function that stores sorted list of character indeces
            indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
            img_res_copy = []
            for idx in indices:
                img_res_copy.append(img_res[idx])  # stores character images according to their index
            img_res = np.array(img_res_copy)

            return img_res

        def segment_characters(image):
            # Preprocess cropped license plate image
            img_lp = cv.resize(image, (500, 300))
            img_gray_lp = cv.cvtColor(img_lp, cv.COLOR_BGR2GRAY)
            _, img_binary_lp = cv.threshold(img_gray_lp, 150, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

            # img_binary_lp = crop_image_only_outside(img_binary_lp)
            plt.imshow(img_binary_lp, cmap='gray')
            # plt.show()

            img_binary_lp = cv.erode(img_binary_lp, (3, 3))
            img_binary_lp = cv.dilate(img_binary_lp, (3, 3))

            LP_WIDTH = img_binary_lp.shape[0]
            print(LP_WIDTH)
            LP_HEIGHT = img_binary_lp.shape[1]
            print(LP_HEIGHT)

            # Make borders white
            img_binary_lp[0:4, :] = 255
            img_binary_lp[:, 0:4] = 255
            img_binary_lp[65:75, :] = 255
            img_binary_lp[:, 330:333] = 255

            # Estimations of character contours sizes of cropped license plates
            dimensions = [LP_WIDTH / 20, LP_WIDTH / 2, LP_HEIGHT / 15, 2 * LP_HEIGHT / 3]
            plt.imshow(img_binary_lp, cmap='gray')
            plt.show()
            # cv.imwrite('contour.jpg', img_binary_lp)

            # Get contours within cropped license plate
            char_list = find_contours(dimensions, img_binary_lp)

            return char_list

        path = self.ImagePath
        char = segment_characters(img)
       # print(len(x_cntr_list))
       # print(x_cntr_list)
        for i in range(len(x_cntr_list)):
        #     plt.subplot(1, 10, i + 1)
        #     plt.imshow(char[i], cmap='gray')
             cv.imwrite(f'{path}+{i}.png', char[i])
        #     plt.axis('off')
        # # plt.show()
        # for i in char:
        #     cv.imshow("hi", i)
        #     cv.waitKey(0)
        #
        return char

    def RunSegmentation(self):
      #  self.GaussianBlur()
        self.Adaptive_Threshold()
        return self.Masking()
