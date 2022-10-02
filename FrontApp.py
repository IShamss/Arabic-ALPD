import sys
import time

from PIL import Image, ImageQt
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QLabel, QSplashScreen

# from detect import crop_one
sys.path.insert(0, './localisation')
path = './localisation/data/images/1.png'
import localisation.detect as detect
from NewSegmentation.segment import segmentChars
from recognition.KNN import predictChars, classify_image_arrays
from integeration.client import endPoint
from localisation.core.functions import load_model
import os
import numpy as np
from datetime import datetime
import glob

btn_pushed = False
frame = 0


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.clean_directory("./green_boxes")
        self.clean_directory("./detections")
        # Load Screen
        uic.loadUi('frontapp.ui', self)
        # logo of window
        self.setWindowIcon(QIcon('logo.ico'))
        # Button
        self.findChild(QPushButton, "startButton").clicked.connect(self.Run)
        # Get Input from each field
        self.input_path = self.findChild(QTextEdit, "inputPath")
        self.findChild(QPushButton, 'skipButton').clicked.connect(self.skipImg)
        self.main_img = self.findChild(QLabel, "mainImage")
        self.main_img.hide()
        self.plate_img = self.findChild(QLabel, "plateImg")
        self.green_img = self.findChild(QLabel, "greenImg")
        self.green_img.hide()
        self.endpoint = self.findChild(QLabel, "endpoint")
        self.Lp = self.findChild(QLabel, "LP")
        self.endpoint.hide()
        self.Lp.hide()
        self.plate_img.hide()
        self.segmented_chars = []
        self.textbox_values = []
        self.images_to_be_saved = []
        for i in range(1, 8):
            self.segmented_chars.append(self.findChild(QLabel, f"seg{i}"))
            # self.textbox_values.append(self.findChild(QTextEdit, f"val{i}"))
        self.clean()
        self.show()

    def Run(self):
        # include prediction code here
        print("Clicked")
        input_path = self.input_path.toPlainText()
        cropped_paths = detect.crop_multiple(input_path, False, saveModel)
        green_paths = "./green_boxes"
        for img, plate_path, box_path in zip(os.scandir(input_path), cropped_paths, os.scandir(green_paths)):
            global btn_pushed
            btn_pushed = False
            self.main_img.show()
            self.green_img.show()
            self.endpoint.show()
            self.Lp.show()
            self.plate_img.show()
            self.Lp.setAlignment(QtCore.Qt.AlignCenter)
            self.endpoint.setAlignment(QtCore.Qt.AlignCenter)
            self.main_img.setScaledContents(True)
            self.main_img.setPixmap(QtGui.QPixmap(img.path))
            self.plate_img.setScaledContents(True)
            self.plate_img.setPixmap(QtGui.QPixmap("./" + plate_path))
            self.green_img.setScaledContents(True)
            self.green_img.setPixmap(QtGui.QPixmap(box_path.path))
            _, chars = segmentChars(plate_path)
            self.labels = predictChars(classify_image_arrays(chars))
            self.findChild(QLabel, "LP").setText(self.labels)
            chars2 = self.labels

            self.labels = self.labels[::-1]
            self.labels = self.labels.split(" ")
            for idx, char in enumerate(chars):
                try:
                    self.segmented_chars[idx].setScaledContents(True)
                    img = Image.fromarray(char).convert('RGB')
                    img = np.array(img)
                    # render the segmented images
                    # self.to_be_saved[img] = self.labels[idx]
                    img = img[:, :, ::-1].copy()
                    image = QtGui.QImage(img, img.shape[1], img.shape[0], img.shape[1] * 3, QtGui.QImage.Format_BGR888)
                    pix = QtGui.QPixmap(image)
                    self.segmented_chars[idx].setPixmap(QtGui.QPixmap(pix))
                    self.textbox_values[idx].setText(self.labels[idx])
                except Exception:
                    continue
            self.findChild(QLabel, "endpoint").setText(endPoint(chars2))
            while (not btn_pushed):
                QtCore.QCoreApplication.processEvents()
        self.finish()

    def finish(self):
        self.main_img.clear()
        self.plate_img.clear()
        self.green_img.clear()
        self.Lp.clear()
        self.endpoint.clear()
        self.main_img.setAlignment(QtCore.Qt.AlignCenter)
        self.main_img.setText("Enter a new input directory")
        self.clean_directory("./green_boxes")
        self.clean_directory("./detections")
        self.clean_directory("./outputs")

    def clean_directory(self, path):
        files = glob.glob(f'{path}/*')
        for file in files:
            os.remove(file)

    def clean(self):
        for label, text in zip(self.segmented_chars, self.textbox_values):
            label.clear()
            text.setText("0")

    def saveImg(self):
        print("Saved")
        mappings = {
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "10": "أ",
            "11": "ب",
            "12": "ج",
            "13": "د",
            "14": "ر",
            "15": "س",
            "16": "ص",
            "17": "ط",
            "18": "ع",
            "19": "ف",
            "20": "ق",
            "21": "ل",
            "22": "م",
            "23": "ن",
            "24": "ه",
            "25": "و",
            "26": "ي",
        }
        key_list = list(mappings.keys())
        val_list = list(mappings.values())
        for result, img in zip(self.textbox_values, self.segmented_chars):
            if result.toPlainText() != "0":
                directory_num = key_list[val_list.index(result.toPlainText())]
                path = self.output_path.toPlainText() + f"/{directory_num}"
                # img=np.array(img.pixmap().toImage())
                image = ImageQt.fromqpixmap(img.pixmap())
                image.save(f"{path}/{str(datetime.now())[-5:]}.jpg")
                # cv2.imwrite(os.path.join(path,f"{datetime.now()}.jpg"),image)

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
            self.progressBar.setValue(i + 1)


# Main
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    saveModel = load_model()

    splash.progress()
    currWindow = UI()
    sys.exit(application.exec_())
