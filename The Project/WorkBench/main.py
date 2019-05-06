import sys

# Basic Qt imports
from PyQt5.QtWidgets import (
            QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QTabWidget, QGridLayout,
            QPushButton, QLabel
)
from PyQt5.QtGui import QColor, QPixmap, QImageReader
from PyQt5.QtCore import Qt
import CubeWindow
import Sandbox
import os

class SubWindow(QWidget):


    def __init__(self, parent = None, length = 500, width = 500):

        super().__init__(parent)
        self.length = length
        self.width = width
        self.initUI(self.length, self.width)


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

        # Central widget in order to be able to add a layout to the main window
        self.centralWidget = SubWindow(self, 1100, 800)
        self.setCentralWidget(self.centralWidget)

        # Main layout (grid is most practical)
        self.mainLayout = QGridLayout()
        # Set minimum width in order to readjust the elements' widths and heights
        self.mainLayout.setColumnMinimumWidth(0, 300)
        self.mainLayout.setColumnMinimumWidth(1, 700)

        # Widget init
            # All about Cube Window
        # Container for layout
        self.cubeContainerWidget = QWidget()
        # Cube window
        self.qOpenGLWidget = CubeWindow.Cube(self, 500, 500)
        # Place holder to reduce the cube windows's height
        self.placeHoldingWidget = QWidget()
        # Layout
        self.cubeLayout = QGridLayout()
        # Readjust cube window's height
        self.cubeLayout.setRowMinimumHeight(1, 700)
        # Add placeHoldingWidget above and below the cube window
        self.cubeLayout.addWidget(self.placeHoldingWidget, 0, 0)
        self.cubeLayout.addWidget(self.qOpenGLWidget, 1, 0)
        self.cubeLayout.addWidget(self.placeHoldingWidget, 2, 0)
        # Set cube container layout
        self.cubeContainerWidget.setLayout(self.cubeLayout)

            # Tabs
        # Tab host
        self.tabs = QTabWidget()
                # Tab 1: Cubes
        self.tabOne = QWidget()
                    # Tab content
        self.tabOneLayout = QVBoxLayout()

        os.chdir('images')
        print(os.path.abspath('thumbnail_3x3.png'))

        self.pixmap3x3 = QPixmap('images/thumbnail_3x3.png')
        if self.pixmap3x3.isNull():
            print("AAALLAAAAARRRMMMMM")

        self.label3x3 = ClickableLabel(self, self.cubeContainerWidget, self.pixmap3x3)
        self.tabOneLayout.addWidget(self.label3x3)
        self.tabOne.setLayout(self.tabOneLayout)
                # Tab 2: Algorithms
        self.tabTwo = QWidget()
            # Add tabs to tab host
        self.tabs.addTab(self.tabOne, "Cubes")
        self.tabs.addTab(self.tabTwo, "Algorithms")

            # Add widgets to main layout
        self.mainLayout.addWidget(self.tabs, 0, 0)
        #self.mainLayout.addWidget(self.cubeContainerWidget, 0, 1)


        # Set mainLayout as the central widgets layout
        self.centralWidget.setLayout(self.mainLayout)
        # Window Title
        self.setWindowTitle("Definitely Not A Rubik's")
        # Window position & dimensions
        self.setGeometry(200, 100, 1100, 800)
        # Show main window
        self.show()


    def keyPressEvent(self, event):

        self.qOpenGLWidget.keyboard(event.key())


    def mousePressEvent(self, event):

        self.qOpenGLWidget.mouseClicked(event)


    def mouseMoveEvent(self, event):

        self.qOpenGLWidget.mouseMoved(event)



class ClickableLabel(QLabel):

    def __init__(self, mainWindow, cubeContainerWidget, pixmap):

        super().__init__()
        self.mainWindow = mainWindow
        self.cubeContainerWidget = cubeContainerWidget
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):

        if not self.mainWindow.mainLayout.itemAt(1):
            self.mainWindow.mainLayout.addWidget(self.cubeContainerWidget, 0, 1)





if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    testWindow = QMainWindow(mainWindow)

    sys.exit(app.exec_())
