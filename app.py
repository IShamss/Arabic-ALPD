from PyQt5 import QtWidgets, uic, QtGui,QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QDialog, QMainWindow, QPushButton, QFrame,QTextEdit,QLabel,QGridLayout
import sys
from PIL import Image
# from detect import crop_one
sys.path.insert(0,'./localisation')
import detect as detect
from NewSegmentation.newSeg import segmentChars
from  recognition.KNN import predictChars , classify_unlabelled_directory
import os
import numpy as np

btn_pushed = False
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load Screen
        uic.loadUi('starter.ui', self)
        # Button
        self.findChild(QPushButton, "startButton").clicked.connect(self.Run)
        # Get Input from each field
        self.input_path = self.findChild(QTextEdit,"inputPath")
        # self.input_path = self.input_path.toPlainText()
        self.output_path = self.findChild(QTextEdit,"outputPath")
        self.output_path = self.output_path.toPlainText()
        self.findChild(QPushButton,'saveButton').clicked.connect(self.saveImg)
        self.findChild(QPushButton,'skipButton').clicked.connect(self.skipImg)
        # QtCore.QObject.connect(save_btn,QtCore.SIGNAL("clicked()"),self.saveImg)
        # QtCore.QObject.connect(skip_btn,QtCore.SIGNAL("clicked()"),self.skipImg)
        # self.function = self.findChild(QLineEdit, "Function")
        # self.minVal = self.findChild(QLineEdit, "Min")
        self.main_img = self.findChild(QLabel,"mainImage")
        self.plate_img = self.findChild(QLabel,"plateImg")
        self.segmented_chars=[]
        self.textbox_values=[]
        for i in range(1,8):
            self.segmented_chars.append(self.findChild(QLabel,f"seg{i}"))
            self.textbox_values.append(self.findChild(QTextEdit,f"val{i}"))
        self.show()

    def Run(self):
        # include prediction code here
        print("Clicked")
        input_path = self.input_path.toPlainText()
        # loop through all images
        cropped_paths = detect.crop_multiple(input_path)
        for img,plate_path in zip(os.scandir(input_path),cropped_paths):
            global btn_pushed
            btn_pushed=False
            self.main_img.setScaledContents(True)
            self.main_img.setPixmap(QtGui.QPixmap(img.path))
            self.plate_img.setScaledContents(True)
            self.plate_img.setPixmap(QtGui.QPixmap("./"+plate_path))
            _,chars = segmentChars(plate_path)
            for idx,char in enumerate(chars):
                self.segmented_chars[idx].setScaledContents(True)
                img=Image.fromarray(char).convert('RGB')
                img = np.array(img) 
                # Convert RGB to BGR 
                img = img[:, :, ::-1].copy() 
                image = QtGui.QImage(img, img.shape[1],img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_BGR888)
                pix = QtGui.QPixmap(image)
                self.segmented_chars[idx].setPixmap(QtGui.QPixmap(pix))

            while(not btn_pushed):
                QtCore.QCoreApplication.processEvents()
        


    def clean(self):
        pass

    
    def saveImg(self):
        print("This is the save button")
        global btn_pushed
        btn_pushed=True

    def skipImg(self):
        print("this is the skip button")
        global btn_pushed
        btn_pushed=True
        


# Main
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    currWindow = UI()
    sys.exit(application.exec_())