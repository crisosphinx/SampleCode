from PySide import QtGui, QtCore
import sys


class Calculator(QtGui.QWidget):
    def __init__(self, parent=None):
        """
        Set up the Calculator Module. This Module will contain
        just the calculator functions.
        That includes:
        -   All buttons can be clicked
        -   Any numbered clicked in the QWidget are translated directly
            into the QLineEdit

        :param parent: Object for which the gui would be parented to
        """

        super(Calculator, self).__init__(parent)
        self.line = QtGui.QLineEdit()
        self.line.setFont(QtGui.QFont('SansSerif', 25))
        _title = 'Calculator'
        self.setWindowTitle(_title)
        self.calculator_form()

    def calculator_form(self, parent=None):
        """
        The actual calculator layout.

        :param parent: Object to parent this module to.
        :return:
        """

        _lay = QtGui.QVBoxLayout(parent)
        _grid = QtGui.QGridLayout()

        # Disable the text line so no one can type into it
        self.line.setDisabled(True)
        self.line.setMaximumHeight(40)
        # Align the text right so it looks readable
        self.line.setAlignment(QtCore.Qt.AlignRight)

        # Create the buttons for actual calculations
        _btn1 = QtGui.QPushButton('1')
        _btn2 = QtGui.QPushButton('2')
        _btn3 = QtGui.QPushButton('3')
        _btn4 = QtGui.QPushButton('4')
        _btn5 = QtGui.QPushButton('5')
        _btn6 = QtGui.QPushButton('6')
        _btn7 = QtGui.QPushButton('7')
        _btn8 = QtGui.QPushButton('8')
        _btn9 = QtGui.QPushButton('9')
        _btn0 = QtGui.QPushButton('0')
        _dot = QtGui.QPushButton('.')
        _left = QtGui.QPushButton('(')
        _right = QtGui.QPushButton(')')
        _enter = QtGui.QPushButton('=')
        _plus = QtGui.QPushButton('+')
        _minus = QtGui.QPushButton('-')
        _multi = QtGui.QPushButton('x')
        _divid = QtGui.QPushButton('/')
        _remove = QtGui.QPushButton('<-')

        # Set Size
        _btn1.setFont(QtGui.QFont('SansSerif', 10))
        _btn2.setFont(QtGui.QFont('SansSerif', 10))
        _btn3.setFont(QtGui.QFont('SansSerif', 10))
        _btn4.setFont(QtGui.QFont('SansSerif', 10))
        _btn5.setFont(QtGui.QFont('SansSerif', 10))
        _btn6.setFont(QtGui.QFont('SansSerif', 10))
        _btn7.setFont(QtGui.QFont('SansSerif', 10))
        _btn8.setFont(QtGui.QFont('SansSerif', 10))
        _btn9.setFont(QtGui.QFont('SansSerif', 10))
        _btn0.setFont(QtGui.QFont('SansSerif', 10))
        _dot.setFont(QtGui.QFont('SansSerif', 10))
        _left.setFont(QtGui.QFont('SansSerif', 10))
        _right.setFont(QtGui.QFont('SansSerif', 10))
        _enter.setFont(QtGui.QFont('SansSerif', 10))
        _plus.setFont(QtGui.QFont('SansSerif', 10))
        _minus.setFont(QtGui.QFont('SansSerif', 10))
        _multi.setFont(QtGui.QFont('SansSerif', 10))
        _divid.setFont(QtGui.QFont('SansSerif', 10))
        _remove.setFont(QtGui.QFont('SansSerif', 10))

        # Connect the functions to the buttons
        _btn1.pressed.connect(lambda: self.add_number('1'))
        _btn2.pressed.connect(lambda: self.add_number('2'))
        _btn3.pressed.connect(lambda: self.add_number('3'))
        _btn4.pressed.connect(lambda: self.add_number('4'))
        _btn5.pressed.connect(lambda: self.add_number('5'))
        _btn6.pressed.connect(lambda: self.add_number('6'))
        _btn7.pressed.connect(lambda: self.add_number('7'))
        _btn8.pressed.connect(lambda: self.add_number('8'))
        _btn9.pressed.connect(lambda: self.add_number('9'))
        _btn0.pressed.connect(lambda: self.add_number('0'))
        _dot.pressed.connect(lambda: self.add_number('.'))
        _enter.pressed.connect(self.solve)
        _left.pressed.connect(lambda: self.add_number('('))
        _right.pressed.connect(lambda: self.add_number(')'))
        _plus.pressed.connect(lambda: self.add_number('+'))
        _minus.pressed.connect(lambda: self.add_number('-'))
        _multi.pressed.connect(lambda: self.add_number('*'))
        _divid.pressed.connect(lambda: self.add_number('/'))
        _remove.pressed.connect(self.remove)

        # Align the buttons on the grid in our scene
        _grid.addWidget(_btn1, 0, 0)
        _grid.addWidget(_btn2, 0, 1)
        _grid.addWidget(_btn3, 0, 2)
        _grid.addWidget(_btn4, 1, 0)
        _grid.addWidget(_btn5, 1, 1)
        _grid.addWidget(_btn6, 1, 2)
        _grid.addWidget(_btn7, 2, 0)
        _grid.addWidget(_btn8, 2, 1)
        _grid.addWidget(_btn9, 2, 2)
        _grid.addWidget(_btn0, 3, 1)
        _grid.addWidget(_dot, 3, 2)
        _grid.addWidget(_left, 4, 1)
        _grid.addWidget(_right, 4, 2)
        _grid.addWidget(_plus, 0, 4)
        _grid.addWidget(_minus, 1, 4)
        _grid.addWidget(_multi, 2, 4)
        _grid.addWidget(_divid, 3, 4)
        _grid.addWidget(_enter, 4, 4)
        _grid.addWidget(_remove, 4, 0)

        # Add everything to the main window
        _lay.addWidget(self.line)
        _lay.addLayout(_grid)
        self.setLayout(_lay)

    def keyPressEvent(self, event):
        # These are the keys we only want to accept... Eval is dangerous
        _accepted_keys = [
            '1', '2', '3', '4', '5',
            '6', '7', '8', '9', '+',
            '-', '/', '*', '.', '(',
            ')'
        ]

        # Get the event.key() / event.text()
        if event.key() == QtCore.Qt.Key_Backspace:
            # "Press <-"
            self.remove()

        elif event.key() == QtCore.Qt.Key_Return:
            # "Press equal sign"
            self.solve()

        else:
            if event.text() in _accepted_keys:
                self.add_number(event.text())

    def enterEvent(self, event):
        # When the mouse enters the QWidget, grab the keyboard
        self.grabKeyboard()

    def leaveEvent(self, event):
        # When the mouse exists the QWidget, make the keyboard input go away
        self.releaseKeyboard()

    def add_number(self, _passed_key=str()):
        # Add the pressed key to the QLineEdit
        _info = self.line.text()
        self.line.setText(_info + _passed_key)

    def solve(self):
        # Solve the information
        _info = float(eval(self.line.text()))
        self.line.setText(str(_info))

    def remove(self):
        # When backspace is hit, remove the last item in the string
        _text = self.line.text()[:-1]
        self.line.setText(_text)


def start():
    _calculator = Calculator()
    return _calculator


def main(argv):
    """
    Start the program.

    :param argv: Passed system arguments.
    :return:
    """

    _app = QtGui.QApplication(argv)
    _main = start()
    _main.show()
    sys.exit(_app.exec_())


if __name__ == '__main__':
    main(sys.argv)
