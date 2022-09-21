from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QDialog, QMainWindow, QPushButton, QFrame,QTextEdit,QLabel,QGridLayout
import sys


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
        # self.function = self.findChild(QLineEdit, "Function")
        # self.minVal = self.findChild(QLineEdit, "Min")
        self.main_img = self.findChild(QLabel,"mainImage")
        # self.maxVal = self.findChild(QLineEdit, "Max")
        # Show Window
        # self.im = QPixmap("./img.jpg")
        # self.label = QLabel()
        # self.label.setPixmap(self.im)

        # self.grid = QGridLayout()
        # self.grid.addWidget(self.label,1,1)
        # self.setLayout(self.grid)

        # self.setGeometry(50,50,320,200)
        # self.setWindowTitle("PyQT show image")
        self.show()

    def Run(self):
        # include prediction code here
        print("Clicked")
        self.main_img.setScaledContents(True)
        self.main_img.setPixmap(QtGui.QPixmap(self.input_path.toPlainText()))
        

    
    def saveImg(self):
        print("This is the save button")
        

    def skipImg(self):
        print("this is the skip button")
        


# Main
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    currWindow = UI()
    sys.exit(application.exec_())