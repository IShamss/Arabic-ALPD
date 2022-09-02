class DetectionCharacter:
    def __init__(self, imgplate):
        self.licensePlate = imgplate
        print("Segmentation Constructor")
    #def GaussianBlur(self,path):
     #   image = cv2.imread(path)
        # apply guassian blur on The image
      #  blurred = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
        # display Blurred image
       # cv2.imwrite(path, blurred)
        # cv2.waitKey(0)  # waits until a key is pressed
        #print("Blurred")
        #return path
    #def Adaptive_Threshold(self,path):
     #   image = cv2.imread(path)
      #  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
       # threshed = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
        #cv2.imwrite(path, threshed)
        #  print("Threshedddd")
        # cv2.waitKey(0)
        #return path
    def masking(self,img):
        print("masking func")

