class DetectionCharacter:
    def __init__(self, imgplate):
        self.licensePlate = imgplate
        print("Segmentation Constructor")

    def removeBluring(self, img):
        print("remove bluring func")

    def thresholding(self, img):
        print("threshold func")

    def masking(self,img):
        print("masking func")

    # def GaussianBlur(path):
    #     image = cv2.imread(path)
    #     # apply guassian blur on The image
    #     blurred = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
    #     # display Blurred image
    #     cv2.imwrite(path, blurred)
    #     # cv2.waitKey(0)  # waits until a key is pressed
    #     print("Blurred")
    #     return path