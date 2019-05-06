import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv) # Application (the big whole thing)
# sys.argv to be able to add parameters when the program starts
window = QWidget() # Window of your application
window.setGeometry(500, 500, 700, 500) # Windows dimensions and upper left corner
window.setWindowTitle("This is only a test") # Windows title
window.setWindowIcon(QIcon("Quadrat.png")) # Windows icon --> Does not work on mac

window.show() # Show the window to the user

sys.exit(app.exec_()) # Programm stops running when closing the window
