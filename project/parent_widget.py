from PySide import QtGui, QtCore
import sys
import webbrowser
from win32api import GetSystemMetrics
from project import *

version = '0.0.001'


class TestWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)

        # Our title
        _title = 'Sample | v.{}'.format(version)

        # When we have more UI Items, create a module that will run checks and
        # pass the results to these dictionaries.
        self.results = dict()
        self.errors = dict()

        # Specify window information, including but not limited to the icon,
        # title, and tab widget that is child to this widget.
        self.icon = QtGui.QIcon('./icon/test.ico')
        self.setWindowTitle(_title)
        self.setWindowIcon(self.icon)
        self.width_ = 1000
        self.height_ = 600
        self.parent = parent
        self.tab = QtGui.QTabWidget(self)

        # Get the system metrics of our screen size
        _x = (GetSystemMetrics(0) / 2) - (self.width_ / 2)
        _y = (GetSystemMetrics(1) / 2) - (self.height_ / 2)

        # Set the location, width and height of our window - should be center.
        self.setGeometry(_x, _y, self.width_, self.height_)
        # Add the tray icon
        self.tray_icon = SystemTrayIcon(self, self.icon)
        # Build our window
        self.creator_ui()

    def creator_ui(self):
        """
        Create a tabwidget window that binds all of our displayed information
        as various tabs on the left-hand side of the screen. This will enable
        us to add multiple widgets whenever we want.

        :return
        """

        # Create the tab widget
        _tab = self.tab
        # Tab shape should be triangular
        _tab.setTabShape(QtGui.QTabWidget.Triangular)
        _tab.setTabPosition(QtGui.QTabWidget.West)
        _tab.setGeometry(0, 0, self.width_, self.height_)
        _lay = QtGui.QVBoxLayout()

        # Set up the forms to be placed in the modules dir
        handlers_mapping = {
            'Calculator': calculator.start(),
            'Notes': notes.start()
        }

        _keys = handlers_mapping.keys()
        _values = handlers_mapping.values()

        for _name, _content in zip(_keys, _values):
            _tab.addTab(_content, _name)

        # Add tabs with the corresponding widgets
        _lay.addWidget(_tab)

        return self

    def closeEvent(self, event):
        # print 'User pressed red X at top right part of the screen.'
        self.tray_icon.hide()
        i = 0
        while i < self.tab.count():
            if i == 0:
                _eachtab = self.tab.children()[i]
                for _eachwidget in _eachtab.children():
                    try:
                        _eachwidget.close()
                    except AttributeError:
                        pass
            i += 1
        # self.parent.close()
        event.accept()


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None, icon=None):
        """
        System Tray Icon builder.

        :param parent: Parent of the icon should be our program
        :param icon: Icon specified
        """

        super(SystemTrayIcon, self).__init__(parent)
        self.parent = parent
        self.icon = icon
        self.start()

    def start(self):
        """
        Start or build our icon in the lower right-hand corner and apply
        a context menu to it.

        :return:
        """

        self.setIcon(self.icon)
        self.setToolTip(
            'Our Tester is Running\nProgram Version: {}'.format(version) +
            '\nJeff3DAnimation.com' +
            '\nUpdates: ?'
        )
        self.setVisible(True)
        _menu = QtGui.QMenu()
        _menu.setStyleSheet(
            'QMenu { background-color: #000000; color: #FFFFFF; ' +
            'border: 3px solid gray; } ' +
            'QMenu::item:selected { background: #FFD700; }'
        )
        self.setContextMenu(_menu)
        _menu.addAction('&Acknowledgements', lambda: Thanks(self.parent))
        _menu.addAction('&Jeff3DAnimation.com', lambda: self.goto_website())
        _menu.addAction('&Quit', self.parent.close)
        self.activated.connect(self.hi)  # self.parent.activateWindow)

    @staticmethod
    def goto_website():
        """
        Launch my website

        :return:
        """

        webbrowser.open('http://www.Jeff3DAnimation.com/')

    def hi(self, event):
        """
        Testing a middle-click event. We can put a fun little thing in here.

        :param event:
        :return:
        """

        if event == self.MiddleClick:
            print "Hello, you've accessed the secret menu."
        elif event == self.Trigger:
            # Normal click will activate the window / place the window
            # in the most forward position / above all other windows on our
            # desktop.
            self.parent.activateWindow()


class Thanks(QtGui.QSplashScreen):
    def __init__(self, parent=None):
        """
        Splash screen that pops up to provide credits. This is going to be
        edited later for revisions. Add an image as the background to keep
        users entertained by what they see / read.

        :param parent:
        """

        super(Thanks, self).__init__(parent)

        _pixmap = QtGui.QPixmap('./documents/isetta.png')
        # Scale the image to be 400 wide
        _size = _pixmap.scaledToWidth(400)
        # Set the new image as the background image
        self.setPixmap(_size)

        # Build the window, show it, focus it and bring it above.
        self.build()
        self.show()
        self.setFocus()
        self.raise_()

        # Get the window size and location
        self.setGeometry(500, 500, _size.width(), _size.height())

    def build(self):
        """
        Build our Acknowledgements Splash Screen.

        :return:
        """

        _layout = QtGui.QVBoxLayout()
        _thanks = QtGui.QLabel('Acknowledgements:\n\n')
        _info = """
Please go to Jeff3DAnimation.com

Copyright (c) Jeff Miller 2019

- Jeff Miller
        """
        _document = QtGui.QLabel()
        _document.setText(_info)

        _thanks.setStyleSheet(
            'color: #000000; font-size: 30px; font-weight: bold; '
        )
        _document.setStyleSheet(
            'background-color: rgba(40, 40, 40, 200); ' +
            'color: #FF2222; font-size: 15px;'
        )

        _thanks.setAlignment(QtCore.Qt.AlignHCenter)
        _document.setAlignment(QtCore.Qt.AlignHCenter)

        _layout.addWidget(_thanks)
        _layout.addWidget(_document)
        self.setLayout(_layout)

    def focusOutEvent(self, event):
        """
        Close the splash screen if it loses focus for whatever reason.

        :param event: Passed event
        :return:
        """

        # If we lose focus of our splash screen, quit it
        self.close()
        event.accept()

    def mousePressEvent(self, event):
        """
        If it gets a click, close it as well. We will consider it losing focus.

        :param event: Passed event
        :return:
        """

        # If we lose focus of our splash screen, quit it
        self.close()
        event.accept()

    def closeEvent(self, event):
        """
        Any close event. Here, we could specify specialized methods to further
        implement our programs user interface. Perhaps create a json that
        documents UI layout.

        :param event: Passed event
        :return:
        """

        event.accept()


def start(parent=None):
    test_window = TestWindow(parent)
    return test_window


def main(argv):
    """
    Start the program.

    :param argv: Passed system arguments.
    :return:
    """

    _app = QtGui.QApplication(argv)
    # Assign the clean looks style to our entire widget and its children.
    _app.setStyle(QtGui.QStyleFactory.create('cleanlooks'))
    _main = start()
    _main.show()
    sys.exit(_app.exec_())


if __name__ == '__main__':
    main(sys.argv)
