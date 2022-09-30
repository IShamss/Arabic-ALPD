### ALPD
> Arabic Automatic License Plate Detector

**IMAGE PROCESSING**

*Description*           

This Python code simply applies the image processing function. To illustrate, image processing means to be able to capture images and extract from it the desired information. In this project we are working on identifying the car plates of any vehicle trying to pass through a resedential compound's gate and check wheather these plates match with the previously recorded data or not. To let this technically work, we had to split the task into three stages. First, localisation, after this phase ends, the image should be pictured and cleared from anything apart from the plates. The second phase is segmentation, in this part, each character on the plate is seperated from the others in order to be predicted easily whatever its' language. At the end there is the recognition phase which directly predicts the plate's characters. To sum up, the input for this system will be a car image while the output will be a string of the characters on the car's plate.

*Dependencies Packages*
- LXML
- tqdm
- absl
- pytesseract
- pillow
- easydict
- pandas
- glob
- numpy
- skimage
- cv2
- collections
- imutils
- tensorflow
- matplotlib
- torch
- torch vision.models
- torch vision.transforms

*Installation*

To install any python library easily, there are few steps than any user should follow:
  1. verify that you can access python in command line.            ![Python_Exit](https://media.github.ibm.com/user/408442/files/99629680-2eca-11ed-9793-75bf0e9cab88)

  2. check that package you need is available on Pypi ( Python's library store) , to be able to use the pip tool.
  3. use the pip tool in the comand line to install any library you want. 
     syntax of pip tool: python -m pip install namelibrary
                         Replace namelibrary by what you want to install
   
     Example:      ![Numpy_Install (1)](https://media.github.ibm.com/user/408442/files/1aba2900-2ecb-11ed-9dc7-74d36522fd50)
     
                               " This is the easy common method of installing any library"
  If any problem occured while installing, visit this link for other methods.
  https://www.hackersfriend.com/articles/how-to-install-python-libraries-without-using-the-pip-command#:~:text=To%20install%20any%20python%20library%20without%20pip%20command%2C,We%27ll%20talk%20about%20this%20process%20step%20by%20step.
  
  *Contributors*
  
  Ahmed Ashraf     ahmedashraf828282@gmail.com
  
  Aly
  
  Mohamed Shams    imohamedshamss@gmail.com
  
  Yehia Ragab      yragab7@gmail.com
  
  Youssef Amr      yousef.toba2001@gmail.com
  
  Ziad Khaled
  
  Ziad Sherif     zsherif308@gmail.com

*Citation*

https://arxiv.org/pdf/2011.14936.pdf

https://drive.google.com/drive/folders/10RC3qTOzaQeMeJFi7h1up1j4W6zY1oOX
