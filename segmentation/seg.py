import cv2
class CharacterDetection:
    def __init__(self, LocalizedImagePath):
        self.ImagePath = LocalizedImagePath
        print("Segmentation Constructor")

    def GaussianBlur(self):
        image = cv2.imread(self.ImagePath)
        blurred = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
        cv2.imwrite(self.ImagePath, blurred)

    def Adaptive_Threshold(self):
        image = cv2.imread(self.ImagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshed = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
        cv2.imwrite(self.ImagePath, threshed)

    def masking(self):
        print("masking func")

