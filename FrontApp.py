import sys

import cv2 as cv
from PIL import Image, ImageQt
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QLabel

# from detect import crop_one
sys.path.insert(0, './localisation')
path = './localisation/data/images/1.png'
from localisation import detect
from NewSegmentation.segment import segmentChars
from recognition.KNN import predictChars, classify_image_arrays
from integeration.client import endPoint
from localisation.core.functions import load_model
import os
import numpy as np
from datetime import datetime
import glob

btn_pushed = False


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # Load Screen
        self.saveModel = load_model()
        self.clean_directory("./green_boxes")
        self.clean_directory("./detections")
        uic.loadUi('frontapp.ui', self)
        # Button
        self.findChild(QPushButton, "startButton").clicked.connect(self.Run)
        # Get Input from each field
        self.input_path = self.findChild(QTextEdit, "inputPath")
        # self.input_path = self.input_path.toPlainText()
        # self.output_path = self.findChild(QTextEdit,"outputPath")
        # self.output_path = self.output_path.toPlainText()
        # self.findChild(QPushButton,'saveButton').clicked.connect(self.saveImg)
        self.findChild(QPushButton, 'skipButton').clicked.connect(self.skipImg)
        # QtCore.QObject.connect(save_btn,QtCore.SIGNAL("clicked()"),self.saveImg)
        # QtCore.QObject.connect(skip_btn,QtCore.SIGNAL("clicked()"),self.skipImg)
        # self.function = self.findChild(QLineEdit, "Function")
        # self.minVal = self.findChild(QLineEdit, "Min")
        self.main_img = self.findChild(QLabel, "mainImage")
        self.main_img.hide()
        self.plate_img = self.findChild(QLabel, "plateImg")
        self.green_img = self.findChild(QLabel, "greenImg")
        self.green_img.hide()
        self.endpoint = self.findChild(QLabel, "endpoint")
        self.Lp = self.findChild(QLabel, "LP")
        self.stream = self.findChild(QLabel, "stream")
        self.capturebtn = self.findChild(QPushButton, "capture").clicked.connect(VideoThread.captureImg)
        self.findChild(QPushButton, "close").clicked.connect(self.shutDown)
        self.findChild(QPushButton, "PushStream").clicked.connect(self.streaming)
        # self.capturebtn.hide()
        self.stream.hide()
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
        # output_path = self.output_path.toPlainText()
        # loop through all images
        # if (not os.path.exists(output_path)) or( not os.path.exists(input_path)):
        #    self.main_img.setText("Please Specify correct paths")
        #    return
        # self.create_directories()
        cropped_paths = detect.crop_multiple(input_path, False, self.saveModel)
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

    def clean_directory(self, path):
        files = glob.glob(f'{path}/*')
        for file in files:
            os.remove(file)

    def streaming(self):
        # self.capturebtn.show()
        self.stream.show()
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def shutDown(self):
        self.stream.hide()
        # self.capturebtn.hide()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.stream.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(531, 331, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def clean(self):
        for label, text in zip(self.segmented_chars, self.textbox_values):
            label.clear()
            text.setText("0")

    # def create_directories(self):
    #    output_path = self.output_path.toPlainText()
    #    for i in range(1,27):
    #        if not os.path.exists(output_path+f"/{i}"):
    #            os.mkdir(output_path+f"/{i}")

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


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.frame = 0

    def run(self):
        # capture from web-camera
        capture = cv.VideoCapture(0)
        while self._run_flag:
            ret, self.frame = capture.read()
            if ret:
                self.change_pixmap_signal.emit(self.frame)

            # if cv.waitKey(1) == ord('q'):
            #     cv.imwrite(path, frame)
            #     break

        # shut down capture system
        capture.release()

    def stop(self):

        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

    def captureImg(self):
        try:
            cv.imwrite(path, self.frame)
        except Exception:
            print("Errorr")


# Main
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    currWindow = UI()
    sys.exit(application.exec_())
