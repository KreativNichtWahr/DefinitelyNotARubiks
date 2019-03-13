import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLCDNumber, QSlider, QLabel, QPushButton
)


class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()


    def initUI(self):

        # Basic example of the signals and slots mechanism
        lcd = QLCDNumber(self)                          # An LCDNumber is a "Liquid Crystal Display" number
        slider = QSlider(Qt.Horizontal, self)           # Creates a horizontal slider

        vBox = QVBoxLayout()
        vBox.addWidget(lcd)
        vBox.addWidget(slider)

        slider.valueChanged.connect(lcd.display)        # Displays the sliders value via the LCD number

                                                        # Event source = slider; Event object = valueChanged (the slider's value), which emits a
                                                        # signal ; Event target = lcd

                                                        # A signal is emitted when a particular event occurs. A slot is any python callable and
                                                        # is called when its connected signal is emitted

        text = "x: N/A, y: N/A"

        self.posLabel = QLabel(text, self)                 # Creates a label
        vBox.addWidget(self.posLabel)

        self.setMouseTracking(True)                     # Is normally disabled, your cursors position is then only tracked when a mouse button
                                                        # has been clicked

        buttonOne = QPushButton("Button 1", self)
        buttonTwo = QPushButton("Button 2", self)

        buttonOne.clicked.connect(self.identifySender)
        buttonTwo.clicked.connect(self.identifySender)
        self.senderLabel = QLabel(self)
        vBox.addWidget(self.senderLabel)

        mainLayout = QGridLayout(self)

        mainLayout.addWidget(buttonOne, 0, 0)
        mainLayout.addWidget(buttonTwo, 0, 1)
        mainLayout.addLayout(vBox, 2, 0)

        self.setLayout(mainLayout)

        self.setGeometry(200, 150, 1100, 800)
        self.setWindowTitle("Signals and slots")
        self.show()


    
    def identifySender(self, event):

        sender = self.sender()
        self.senderLabel.setText("{} was pressed".format(sender.text()))


    def mouseMoveEvent(self, event):                    # Another event handler we reimplement

        x = event.x()                                   # The event object stores the x and y values of the cursors coordinates
        y = event.y()

        text = "x: {}, y: {}".format(x, y)
        self.posLabel.setText(text)                        # Updates the label, although it is not very fluid


    # Reimplementing event handler
    def keyPressEvent(self, event):                     # The keyPressEvent handler ALREADY EXISTS, you only REIMPLEMENT it, i.e changing its
                                                        # reaction to a certain event. This handler for instance only handles events which refer
                                                        # to keys being pressed.

        if event.key() == Qt.Key_Escape:                # An event has a lot of attributes, which are all stored in the event variable. In this
                                                        # case, one of them is "key", telling the method which key has been pressed.

                                                        # Qt.Key_Escape = escape key

            self.close()                                # Closes the QWidget, and, as it is the top widget of the application, the application



if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = Window()

    sys.exit(app.exec_())
