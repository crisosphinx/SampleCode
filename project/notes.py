from PySide import QtGui
import widget_lister as dtwl
import widget_creator as dtwc
import sys
import os
import json_loader as jsonl

journal_loc = './documents/journal.json'


class Journal(QtGui.QWidget):
    def __init__(self, parent=None):
        """
        Set up the Journal Module. This Module will contain
        just the journal functions.
        That includes:
        -   Save function
        -   Automatic Load function
        -   Documenting / Ability to write for each session

        :param parent: Object to parent this module to.
        """

        super(Journal, self).__init__(parent)

        # Sets the window title
        self.setWindowTitle('Journal')

        # Location of the journal entries
        self.journal = journal_loc
        self.tab = dtwc.TabCreator()
        self.journal_form()

    def closeEvent(self, event):
        # print 'User pressed red X at top right part of the screen.'
        self.save()
        event.accept()

    def journal_form(self, parent=None):
        """
        The actual journal layout

        :param parent: Object to parent this module to.
        :return:
        """

        _lay = QtGui.QVBoxLayout(parent)

        _menubar = QtGui.QMenuBar()
        _menu = QtGui.QMenu('RESET')
        _menu.addAction('Reset Journal')
        _menu.triggered.connect(self.reset)
        _menubar.addMenu(_menu)

        # The actual journal
        _journal = QtGui.QTextEdit

        # Set the first page
        self.tab.add_page(_journal, 'Page1')

        # Set the blank page
        self.tab.add_page(_journal, None)

        # Set the save button
        _saver = QtGui.QPushButton('Save')

        # Save button function
        _saver.pressed.connect(self.save)
        _menu.triggered.connect(self.reset)

        # Set the layout
        _lay.addWidget(_menubar)
        _lay.addWidget(self.tab)
        _lay.addWidget(_saver)
        self.setLayout(_lay)

        # Load in the information
        if os.path.isfile(self.journal):
            self.load()

    def load(self):
        # Load function
        _info = jsonl.main(load=True, _file=self.journal)
        _set = [int(x) for x in _info.keys()]
        _set.sort()

        # Load in the information per page
        for _key in _set:
            _add = _info[str(_key)]
            self.tab.setCurrentIndex(_key)
            self.tab.widget(_key).setText(str(_add[0]))

        # Opens last page / sets the index to the last page so we can recap
        if self.tab.count() > 2:
            self.tab.setCurrentIndex(_set[-1])
        else:
            pass

    def reset(self):
        if os.path.isfile(self.journal):
            os.remove(self.journal)

    def save(self):
        # Get all the information and save it to the json document
        _info = self.get_information()
        jsonl.main(load=False, _file=self.journal, content=_info)

    def get_information(self):
        pages = dict()

        i = 0
        # Count the tabs
        while i < self.tab.count():
            # Get the first widget per tab (the only one)
            _tab = self.tab.widget(i)
            _text = dtwl.main(_tab)
            if len(_text) == 2:
                if _text[0][0] != '':
                    # Get and save information to the dictionary
                    pages.setdefault(i, []).append(_text[0][0])
            i += 1

        return pages


def start():
    _journal = Journal()
    return _journal


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
