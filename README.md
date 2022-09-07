### ALPD
> Arabic Automatic License Plate Detector

**IMAGE PROCESSING**

*Description*

This code simply applies the image processing function. To illustrate, image processing means to be able to capture images and extract from it the desired information. In this project we are working on identifying the car plates of any vehicle trying to pass through a resedential compound's gate and check wheather these plates match with the previously recorded data or not. To let this technically work, we had to split the task into three stages. First, localization, after this phase ends, the image should be pictured and cleared from anything apart from the plates. The second phase is segmentation, in this part, each character on the plate is seperated from the others in order to be predicted easily whatever its' language. At the end there is the prediction phase which simply predicts the plate's characters.

*Dependencies Packages*
- numpy
- skimage
- cv2
- collections
- imutils
- tensorflow


