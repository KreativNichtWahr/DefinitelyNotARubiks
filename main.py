import sys

# Basic Qt imports
from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QApplication, QVBoxLayout
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
#from OpenGLCube import OpenGLCube
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

        '''self.newCube = OpenGLCube(
                vertices = [(1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
                            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)],
                edges = [(0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3),
                        (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)]
        )
        self.newCube.setMinimumSize(300, 300)

        VBox = QVBoxLayout()
        VBox.addWidget(self.newCube)
        centralWidget.setLayout(VBox)'''

        self.setMouseTracking(True)

        self.setWindowTitle("3D Rubik's Cube Simulator")
        self.setGeometry(200, 100, 1100, 800)
        self.show()


    def keyPressEvent(self, event):

        if event.key() == Qt.Key_S:

            print("That's the right event and it has been caught")
            cmd = "python3 Play_Ground.py"
            sp.Popen(cmd, stdout=sp.PIPE, shell=True)





if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    testWindow = QMainWindow(mainWindow)

    sys.exit(app.exec_())
