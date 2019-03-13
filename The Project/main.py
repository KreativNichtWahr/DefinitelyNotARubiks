import sys

# Basic Qt imports
from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QApplication, QVBoxLayout
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import CubeWindow as cw
import subprocess as sp

class SubWindow(QWidget):


    def __init__(self, length = 400, width = 250, parent = None):

        super().__init__(parent)

        self.initUI(length, width)


    def initUI(self, length, width):

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(100, 100, 100))
        self.setPalette(palette)

        self.resize(length, width)
        self.show()



class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()
        self.initUI()


    def initUI(self):

        centralWidget = SubWindow(parent = self)
        self.setCentralWidget(centralWidget)

        self.setMouseTracking(True)

        self.cubeWindow = cw.Cube(self)

        self.setWindowTitle("3D Rubik's Cube Simulator")
        self.setGeometry(200, 100, 1100, 800)
        self.show()


    def keyPressEvent(self, event):

        self.cubeWindow.keyboard(event.key())

        """if event.key() == Qt.Key_S:

            print("That's the right event and it's been caught")
            cmd = "python3 CubeWindow.py"
            sp.Popen(cmd, stdout=sp.PIPE, shell=True)
        """




if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    testWindow = QMainWindow(mainWindow)

    sys.exit(app.exec_())
