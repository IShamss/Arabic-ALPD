import glob
import sys
import time

from PIL import Image, ImageQt
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QLabel, QComboBox, QSplashScreen

# from detect import crop_one
sys.path.insert(0, './localisation')
import detect as detect
from NewSegmentation.segment import segmentChars
from recognition.KNN import predictChars, classify_image_arrays
from localisation.core.functions import load_model
import os
import numpy as np
from datetime import datetime

btn_pushed = False


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load Screen
        uic.loadUi('labellingapp2.ui', self)
        # logo of window
        self.setWindowIcon(QIcon('logo.ico'))
        # Button
        self.findChild(QPushButton, "startButton").clicked.connect(self.Run)
        # Get Input from each field
        self.input_path = self.findChild(QTextEdit, "inputPath")
        self.output_path = self.findChild(QTextEdit, "outputPath")
        self.findChild(QPushButton, 'saveButton').clicked.connect(self.saveImg)
        self.findChild(QPushButton, 'skipButton').clicked.connect(self.skipImg)
        self.findChild(QPushButton, 'incorrect').clicked.connect(self.increment_incorrect)
        self.main_img = self.findChild(QLabel, "mainImage")
        self.plate_img = self.findChild(QLabel, "plateImg")
        self.incorrect_num_label = self.findChild(QLabel,"incorrectNum")
        # to enable the increment of incorrect images
        self.enable_increment=True
        self.segmented_chars = []
        self.combo_values = []
        self.images_to_be_saved = []
        self.image_count=0
        self.incorrect_count=0
        for i in range(1, 8):
            self.segmented_chars.append(self.findChild(QLabel, f"seg{i}"))
            self.combo_values.append(self.findChild(QComboBox, f"val{i}"))
        self.clean()
        self.populate_values()
        self.show()


    def populate_values(self):
        values=[str(i) for i in range(0,10)]
        values.extend(["أ","ب","ج","د","ر","س","ص","ط","ع","ف","ق","ل","م","ن","ه","و","ى"])
        for box in self.combo_values:
            box.addItems(values)
            # box.currentTextChanged.connect(self.increment_incorrect)

    def increment_incorrect(self):
        if self.enable_increment:
            self.incorrect_count+=1
            self.enable_increment=False
            self.incorrect_num_label.setText(f"Incorrect : {self.incorrect_count}")

    def Run(self):
        # include prediction code here
        print("Clicked")
        input_path = self.input_path.toPlainText()
        output_path = self.output_path.toPlainText()
        # loop through all images
        if (not os.path.exists(output_path)) or (not os.path.exists(input_path)):
            self.main_img.setText("Please Specify correct paths")
            return
        self.create_directories()
        cropped_paths = detect.crop_multiple(input_path, False, saveModel)
        for img, plate_path in zip(os.scandir(input_path), cropped_paths):
            global btn_pushed
            btn_pushed = False
            self.main_img.setScaledContents(True)
            self.main_img.setPixmap(QtGui.QPixmap(img.path))
            self.plate_img.setScaledContents(True)
            self.plate_img.setPixmap(QtGui.QPixmap("./" + plate_path))
            _, chars = segmentChars(plate_path)
            self.labels = predictChars(classify_image_arrays(chars))
            self.image_count+=1
            self.labels = self.labels[::-1]
            self.labels = self.labels.split(" ")
            for idx, char in enumerate(chars):
                try:
                    self.segmented_chars[idx].setScaledContents(True)
                    img = Image.fromarray(char).convert('RGB')
                    img = np.array(img)
                    # render the segmented images
                    img = img[:, :, ::-1].copy()
                    image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_BGR888)
                    pix = QtGui.QPixmap(image)
                    self.segmented_chars[idx].setPixmap(QtGui.QPixmap(pix))
                    # set the values of the combobox
                    index = self.combo_values[idx].findText(self.labels[idx], QtCore.Qt.MatchFixedString)
                    if index >= 0:
                        self.combo_values[idx].setCurrentIndex(index)
                except Exception:
                    continue
            while (not btn_pushed):
                QtCore.QCoreApplication.processEvents()
        self.finish()

    def finish(self):
        self.main_img.clear()
        self.plate_img.clear()
        self.main_img.setAlignment(QtCore.Qt.AlignCenter)
        self.main_img.setText("Enter a new input directory\nAccuracy : {:.2f} %".format((self.incorrect_count / self.image_count)*100))
        self.image_count=0
        self.incorrect_count=0
        self.clean_directory("./green_boxes")
        self.clean_directory("./detections")
        self.clean_directory("./outputs")
        self.clean_directory("./localisation/data/images")
    def clean_directory(self, path):
        files = glob.glob(f'{path}/*')
        for file in files:
            os.remove(file)
    def clean(self):
        for label, text in zip(self.segmented_chars, self.combo_values):
            # text.disconnect()
            label.clear()
            text.setCurrentIndex(0)
            self.enable_increment=True
            # text.currentTextChanged.connect(self.increment_incorrect)

    def create_directories(self):
        output_path = self.output_path.toPlainText()
        for i in range(1, 27):
            if not os.path.exists(output_path + f"/{i}"):
                os.mkdir(output_path + f"/{i}")

    def saveImg(self):
        print("Saved")
        for result, img in zip(self.combo_values, self.segmented_chars):
            selected_idx=result.currentIndex()
            if selected_idx != 0:
                path = self.output_path.toPlainText() + f"/{selected_idx}"
                image = ImageQt.fromqpixmap(img.pixmap())
                image.save(f"{path}/{str(datetime.now())[-5:]}.jpg")

        global btn_pushed
        btn_pushed = True
        self.clean()

    def skipImg(self):
        print("this is the skip button")
        global btn_pushed
        btn_pushed = True
        self.to_be_saved = {}
        self.clean()
class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        uic.loadUi("loading.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        pixmap = QPixmap("IC.png")
        self.setPixmap(pixmap)
        
        self.show()


    def progress(self):

        for i in range(100):
            time.sleep(0.02)
            self.progressBar.setValue(i+1)

# Main
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    saveModel = load_model()

    splash.progress()
    currWindow = UI()
    sys.exit(application.exec_())
