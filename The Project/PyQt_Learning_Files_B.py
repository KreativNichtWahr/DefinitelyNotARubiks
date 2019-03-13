import sys
from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QApplication, QToolTip, QPushButton,
        QMessageBox, QAction, qApp, QMenu, QHBoxLayout, QVBoxLayout,
        QGridLayout, QLabel, QLineEdit, QTextEdit
)                                                                       # Basic Widgets located in PyQt5.QWidgets module
from PyQt5.QtGui import QIcon, QFont


# First simple class - Contains First Programs and Layout management (Zetcode tutorial)

class Window(QWidget):                          # Class to create a window for your application (inherits from QWidget)


    def __init__(self, key, parent = None):                 # Constructor

        super().__init__(parent)                # Calls the parent class's constructor to be able to use its methods

        self.initUI(key)                           # Calls the class's only method, initUI


    def initUI(self, key):                                  # Method which creates some default settings (creates the window)

        QToolTip.setFont(QFont("Arial", 10))           # Font used to render (= berechnen, erzeugen) tooltips

        self.setToolTip("This is a <b>QWidget</b> widget")         # Shows up when hovering over the Window object, i.e., the window

        btn = QPushButton("Quit", self)                            # Creates a Button object whith text = "Button" which "belongs" to the Window object created
        btn.setToolTip("This is a <b>QPushButton</b> widget")      # Shows up when hovering over the Button (<b></b> means "bold")
        btn.clicked.connect(QApplication.instance().quit)          # "clicked" is a signal (signal and slot system) connected to the quit() method
        btn.resize(btn.sizeHint())                                 # Resizes the Button according to the window's dimensions (sizeHint())
        btn.move(250, 175)                                # Moves the Button to (x = 50, y = 50)

        # Buttons
        okButton = QPushButton("OK")                            # "self" attribute missing because you don't simply want to place the
                                                                # button inside the window
        cancelButton = QPushButton("Cancel")

        # Layouts - Can only be placed inside of a QWidget, it is not compatible with QMainWindow!
        if key == "hOrVBox":

            hBox = QHBoxLayout()                                    # Creates a horizontal Layout, i.e a layout where items placed are
                                                                    # alligned horizontally
            hBox.addStretch(1)                                      # Adds a stretchfactor of 1, i.e a strechable space on the left
                                                                    # part of the HBox, which pushes the buttons to the right of the layout
            hBox.addWidget(okButton)                                # Adds the button to the layout
            hBox.addWidget(cancelButton)

            vBox = QVBoxLayout()                                    # Creates a vertical layout
            vBox.addStretch(1)                                      # Same as for the HBox
            vBox.addLayout(hBox)                                    # Adds the HBox to the VBox

            self.setLayout(vBox)                                # Sets the window's layout

        elif key == "grid":

            grid = QGridLayout()                                    # Creates a grid layout, i.e a layout which works with columns and rows
            grid.setSpacing(10)

            buttonLabels = [                                        # List of button labels
                    'Clear', 'Back', '', 'Close',
                     '7', '8', '9', '/',
                    '4', '5', '6', '*',
                     '1', '2', '3', '-',
                    '0', '.', '=', '+'
            ]

            positions = [(i, j) for i in range(5) for j in range(4)]        # List of positions, stored as (y,x) coordinates, i.e a list
                                                                            # of tuples

            for buttonLabel, position in zip(buttonLabels, positions):      # zip() creates an iterable of the form (first, second),
                                                                            # (first, second)

                if buttonLabel == "":                                       # No button needed here
                    continue

                button = QPushButton(buttonLabel)
                grid.addWidget(button, *position)                           # * = variadic arguments, which means that the position tuple
                                                                            # gets unpacked and the row and the column index is passed to
                                                                            # the function

            self.setLayout(grid)

        else:

            title = QLabel('Title')                          # Creates a basic label which says "Title"
            author = QLabel('Author')
            review = QLabel('Review')

            titleEdit = QLineEdit()                          # Creates an line where the user can type in stuff
            authorEdit = QLineEdit()
            reviewEdit = QTextEdit()                         # Creates an area where the user can type in stuff, which can be expanded
                                                             # to the bottom by the user himself by adding a newline or manually by
                                                             # increasing its rowspan

            grid = QGridLayout()
            grid.setSpacing(10)

            grid.addWidget(title, 1, 0)
            grid.addWidget(titleEdit, 1, 1)

            grid.addWidget(author, 2, 0)
            grid.addWidget(authorEdit, 2, 1)

            grid.addWidget(review, 3, 0)
            grid.addWidget(reviewEdit, 3, 1, 5, 1)           # The last two arguments define respectively the features "rowspan" and
                                                             # "columnspan", which influences the amount of rows or columns the widget
                                                             # will occupy

            self.setLayout(grid)


        self.resize(350, 250)                          # Resizes the window
        self.move(0, 50)
        #self.center()                                  # Custom method to center the window which does not work because the class
                                                        # is obsolete
        #self.setWindowTitle("PyQt5")                   # Sets the window's title
        #self.setWindowIcon(QIcon("exit.jpeg"))         # Sets an icon to the left of the WindowTitle (does not work on mac)
        self.show()                                     # Makes the window appear on the screen



    #def center(self):                                   # Simply no working because the module used (QDesktopWidget) is obsolete



# Second, a little more advanced class - Contains Menus and Toolbars (Zetcode tutorial)

class MainWindow(QMainWindow):                  # Class to create a MainWindow for your application (inherits from QMainWindow),
                                                # different becaus it can contain a menubar, toolbar and statusbar

    def __init__(self, x = 200, y = 100, length = 1100, width = 800):

        super().__init__()

        self.initUI(x, y, length, width)


    def initUI(self, x, y, length, width):

        # As you can't put any layout inside of the QMainWindow directly, you need to add a QWidget instead and make it the central
        # widget, i.e one which occupies the whole Window???
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        grid = QGridLayout()

        grid.setSpacing(10)

        centralWidget.setLayout(grid)

        # A simple way to create a subwindow
        hVSubWindow = Window("hOrVBox", parent = self)
        gridSubWindow = Window("grid", parent = self)
        elseSubWindow = Window("else", parent = self)

        grid.addWidget(hVSubWindow, 0, 0)
        grid.addWidget(gridSubWindow, 0, 2, 1, 2)
        grid.addWidget(elseSubWindow, 1, 0)

        # Actions
        exitAct = QAction(QIcon('exit.jpeg'), '&Exit', self)    # Used to perform actions with menubars, toolbars or custom keyboard
                                                                # shortcuts, this QAction will be attributed to some other item
        exitAct.setShortcut('Ctrl+Q')                           # Sets a shortcut for the action (! is still "cmd + Q" for mac users)
        exitAct.setStatusTip('Exit application')                # When hovering over the action in the menu, shows the message
                                                                # "Exit application" in the statusbar
        exitAct.triggered.connect(qApp.quit)                    # Connect the action to the quit() method of the qApp module


        impAct = QAction("Import mail", self)                   # Another action


        viewStatusBarAct = QAction("Show Statusbar", self, checkable = True)      # Action for the checkmenu, lets a checkbox appear
                                                                                  # next to it, which you can interact with
        viewStatusBarAct.setChecked(True)                                         # The action is already checked when the window is
                                                                                  # built
        viewStatusBarAct.setStatusTip("Hide Statusbar")
        viewStatusBarAct.triggered.connect(self.toggleStatusBarOnOf)


        # Menubar
        menubar = self.menuBar()                                # Creates a brandnew menubar
        menubar.setNativeMenuBar(False)                         # For Mac users, to prevent shit


        # Menus
        fileMenu = menubar.addMenu('&File')            # Creates and adds a new menu to the menubar which displays "File"
        fileMenu.addAction(exitAct)                # Adds an the action which has been defined to the new menu created

            # Submenus
        impMenu = QMenu("Import", self)            # Creates a Menu without adding it to the menubar
        impMenu.addAction(impAct)                  # impAct gets added to the menu created above

        fileMenu.addMenu(impMenu)                  # Adds the impMenu to the fileMenu, which makes the impMenu a submenu

            # Checkmenus
        viewMenu = menubar.addMenu("View")
        viewMenu.addAction(viewStatusBarAct)

        # Statusbar
        self.statusBar = self.statusBar()                 # Creates the statusbar...
        self.statusBar.showMessage("Look it's here")      # ...and makes it display the message "Look it's here"

        # Toolbar
        self.toolBar = self.addToolBar("Exit")            # The toolbar is created and displayed via the addToolBar method
        self.toolBar.addAction(exitAct)                   # The already defined action is added to the toolbar

        # Standard settings
        self.setGeometry(x, y, length, width)
        self.setWindowTitle("Statusbar, Menubar, Menus, Submenus")
        self.show()

    def toggleStatusBarOnOf(self, state):

        if state:
            self.statusBar.show()

        else:
            self.statusBar.hide()

        # Context menus
    def contextMenuEvent(self, event):                      # Just like the closeEvent method, this is a method you reimplement,
                                                            # which means, that it already knows what event to react to
        contextMenu = QMenu(self)                                      # A regular QMenu object
        newAct = contextMenu.addAction("New")                          # Simply adds new actions to the menu
        openAct = contextMenu.addAction("Open")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))      # The context menu is displayed with the exec_() method,
                                                                       # it appears at the events location, i.e the cursor's
                                                                       # when you right click, mapToGlobal translates the widget's
                                                                       # to the screen's coordinates
        if action == quitAct:
            qApp.quit()


    # Method which runs when you press the cross to exit
    def closeEvent(self, event):                                    # closeEvent is an event handler

        reply = QMessageBox.question(self, "Message",               # Creates a QMessageBox which appears on your screen, has the title
                "Are your sure to quit?", QMessageBox.Yes |         # "Message", contains a label (text = "Are you sure to quit?") and two
                QMessageBox.No, QMessageBox.No)                     # buttons (Yes and No, No choosen by default), reply stores your answer

        if reply == QMessageBox.Yes:                                 # If you clicked the "Yes" button
            event.accept()                                          # let the event take place

        else:                                                       # Otherwhise
            event.ignore()                                          # ignore it


if __name__  == "__main__":

    app = QApplication(sys.argv)                    # Necessary (= Whole GUI if you will)
    pri_w = MainWindow()                            # Creates a QMainWindow object, i.e, the main window
    #sec_w = Window()                           # Creates a Window object, i.e., a window

    sys.exit(app.exec_())                           # Event handling starts from here (= Mainloop receives events), Stops when exit()
                                                    # is called or the main Widget window (normally the window) is destroyed,
                                                    # sys.exit() = clean exit


# Alternative to the proper OOP version + general alternatives to some methods
"""

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = QWidget()                           # Creates a QWidget object directly
    w.setGeometry(300, 150, 1000, 800)      # Sets the position (first 2 args) and the size (last 2 args) of the object, combination of the resize() and move() methods
    w.resize(800, 1000)                     # Resizes the window
    w.move(300, 200)                        # Moves the window to (x = 300, y = 200)
    w.setWindowTitle("PyQt5")               # Same as above
    w.show()                                #       "

    sys.exit(app.exec_())                   #       "

"""
