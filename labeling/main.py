from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QWidget, QDialog, QMainWindow, QPushButton, QLineEdit,QTextEdit
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
        # self.function = self.findChild(QLineEdit, "Function")
        # self.minVal = self.findChild(QLineEdit, "Min")
        # self.maxVal = self.findChild(QLineEdit, "Max")
        # Show Window
        self.show()

    def Run(self):
        # include prediction code here
        print("Clicked")
        print(self.input_path.toPlainText())


# Main
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    currWindow = UI()
    sys.exit(application.exec_())