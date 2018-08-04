from PySide import QtGui, QtCore
import sys


class Create:
    def __init__(self):
        """

        """

    @staticmethod
    def labeler(
            _text=str(),
            _text2=str(),
            _label=bool(),
            _line=bool(),
            _combo=bool(),
            _drp_btn=bool(),
            _check=bool(),
            _block=bool(),
            _button=bool(),
            _hor_ver=bool(),
            _menu=None
    ):
        """
        Label creator

        :param _text: Text to be added
        :param _text2: Second text to be added
        :param _label: Are we creating a label?
        :param _line:  Are we creating a line edit?
        :param _combo: Are we creating a combobox?
        :param _drp_btn: Are we creating a drop-menu button?
        :param _check: Are we creating a checkbox?
        :param _block: Are we creating a text block?
        :param _button: Are we creating a standard button?
        :param _hor_ver: Alignment of title and widget true/false respectively
        :param _menu: Specified menu for drop-menu button
        :return:
        """

        # Determine if horizontal or vertically stacked
        if _hor_ver is True:
            _box = QtGui.QHBoxLayout()
        else:
            _box = QtGui.QVBoxLayout()

        # Add the text to be displayed with the object
        _lbl = QtGui.QLabel(_text)
        _elem = None

        if _label is True:
            _lbl2 = QtGui.QLabel(_text2)
            _elem = _lbl2

        # Is it a line edit?
        if _line is True:
            _elem = QtGui.QLineEdit()

        # Is it a combobox?
        if _combo is True:
            _elem = QtGui.QComboBox()

        # Is it a button?
        if _drp_btn is True or _button is True:
            _elem = QtGui.QPushButton(_text)
            # Does it have a dropdown menu?
            if _drp_btn is True:
                _elem.setMenu(_menu)

        # Is it a checkbox?
        if _check is True:
            _elem = QtGui.QCheckBox()

        # Is it a textblock?
        if _block is True:
            _elem = QtGui.QTextEdit()

        # Parent them to the layout
        _box.addWidget(_lbl)
        if _elem is not None:
            _box.addWidget(_elem)

        # Return the name of the layout
        return _box


class TabBar(QtGui.QTabBar):
    def __init__(self, parent=None):
        """
        Tab bar gui with allows you to modify the name of the tab.

        :param parent: Parent this TabWidget to the passed parent variable.
        """

        super(TabBar, self).__init__(parent)

        self._editor = QtGui.QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handle_editing_finished)
        self._editor.installEventFilter(self)

    def mouseDoubleClickEvent(self, event):
        """
        Double-click event for the tab.

        :param event:
        :return:
        """

        # Get the tab under the cursor
        _index = self.tabAt(event.pos())
        if _index >= 0:
            # Start the edit
            self.edit_tab(_index)

    def eventFilter(self, widget, event):
        """
        Filter the current events. In this case, we install the event for
        editing the tab. If the tab is double-clicked, add a temporary
        textbox over the tab and allow us to rename the tab after enter is
        pressed. We want to add the ability to exit the textbox.

        :param widget: The passed widget we are parenting the event to
        :param event: The passed event.
        :return:
        """

        if (
                (
                    # If the event is a mouse button press
                    event.type() == QtCore.QEvent.MouseButtonPress and
                    not self._editor.geometry().contains(event.globalPos())
                ) or
                (
                    # If the key press is escape to exit the text box
                    event.type() == QtCore.QEvent.KeyPress and
                    event.key() == QtCore.Qt.Key_Escape
                )
        ):
            # Hide the editor please
            self._editor.hide()
            return True

        return QtGui.QTabWidget.eventFilter(self, widget, event)

    def edit_tab(self, _index):
        """
        Create the edit tab editor text box.

        :param _index:
        :return:
        """

        # Rectangle created
        _rect = self.tabRect(_index)
        self._editor.setFixedSize(_rect.size())
        # Move the global location to the top of the tab
        self._editor.move(self.parent().mapToGlobal(_rect.topLeft()))
        # Add a blank editor to the tab. Select outside of it to deselect.
        self._editor.setText('')  # self.tabText(_index))
        if not self._editor.isVisible():
            # Show the editor if it is not visible
            self._editor.show()

    def handle_editing_finished(self):
        """
        Tab handler. We will use this to edit the tab text.

        :return:
        """

        _index = self.currentIndex()
        if _index >= 0:
            self._editor.hide()
            self.setTabText(_index, self._editor.text())


class TabCreator(QtGui.QTabWidget):
    def __init__(self, parent=None):
        """
        Tab gui with customized functionalities to create a journal-like
        interface. When a page is created, we add a new page named "+".

        When clicked on it, it creates new page with the pre-made QTextEdit.

        :param parent: Parent this TabWidget to the passed parent variable.
        """

        super(TabCreator, self).__init__(parent)
        self.temp = None
        self.tabbar = TabBar(self)
        self.tabbar.setTabsClosable(False)
        self.setTabBar(self.tabbar)
        self.menu = QtGui.QMenu()

        # Set the tab shape to a trapezoid-like shape
        self.setTabShape(QtGui.QTabWidget.Triangular)
        # Faced north.
        self.setTabPosition(QtGui.QTabWidget.North)
        self.currentChanged.connect(
            lambda: self.new_page(self.temp, None)
        )
        self.tabCloseRequested.connect(
            self.gettab
        )

    def gettab(self, event):
        """
        Get the current tab

        :param event: Get the tab selected
        :return:
        """

        _current_tab = event
        _tabname = self.tabbar.tabText(_current_tab)
        self.removeTab(_current_tab)
        print 'Removed {}'.format(_tabname)

    def mousePressEvent(self, event):
        """
        Create a mouse press event to get the mouse press. We want to add
        add or remove buttons from the context menu so we can appropriately
        have specific functions assigned to the particular tab.

        :param event: Mouse button pressed (any)
        :return:
        """

        if event.MouseButtonPress == QtCore.Qt.RightButton:
            # We only want to achieve the right-click button so we can edit it
            # Clear the menu
            self.menu.clear()
            _current_tab = self.tabbar.tabAt(event.pos())
            _amount = self.tabbar.count()
            # If the current tab pressed is two from the end
            if _current_tab == _amount - 2:
                # Deletes tab and makes a new one that is blank
                self.menu.addAction(
                    'Refresh Tab? This will delete all current info.',
                    lambda: self.removeTab(_current_tab)
                )

            # If the tab pressed is three or more from the end
            elif _current_tab <= _amount - 3:
                # Offer the delete tab button
                self.menu.addAction(
                    'Delete Tab',
                    lambda: self.removeTab(_current_tab)
                )

            else:
                # "+" cannot be deleted, add that button
                self.menu.addAction('You cannot delete this tab.')

            # Show the menu
            self.menu.show()
        event.accept()

    def add_page(self, *args):
        """


        :param args:
        :return:
        """

        self.temp = args[0]
        if args[1] is None:
            self.addTab(args[0](), '+')
        else:
            self.addTab(args[0](), args[1])

    def new_page(self, *args):
        """
        Add a new tab / page and create a new tab named "+". This will allow
        for creating new tabs on cue.

        :param args: The passed child gui element. Add whatever you want.
        :return:
        """

        # Get the number of pages
        self.setCurrentIndex(self.count())
        _number = self.count()
        if args[0] is None:
            # print isinstance(self.widget(0), QtGui.QTableWidget)
            _gui = self.temp
        else:
            _gui = args[0]

        # If the current tab is the plus symbol, make a new page
        if self.tabText(self.currentIndex()) == '+':
            # Set the tab text to a page # dependent on the # of current pages
            self.setTabText(self.currentIndex(), 'Page{}'.format(_number))
            self.add_page(_gui, args[1])


def main(argv):
    """
    Run the main application test gui. This provides a tabbed window with the
    ability to infinitely create more tabs on cue. This will be helpeful for
    other parts of my program.

    :param argv: Passed arguments.
    :return:
    """

    _app = QtGui.QApplication(argv)
    _main = TabCreator()
    _main.add_page(QtGui.QLineEdit, 'test')
    _main.add_page(QtGui.QLineEdit, None)
    _main.show()
    sys.exit(_app.exec_())


if __name__ == '__main__':
    main(sys.argv)
