from PySide import QtGui
from PySide import QtCore
import py_compile as pyc
import os
import sys
import datetime
import subprocess
import shutil
import __version__
import checkForVersion
import parser
import subprocess
import jsonReader
import jsonWriter

enabled = list()
try:
    import build_entire_work_dir_listing as bewdl  # Shortened, too long
except ImportError:
    enabled.append(0)
    pass

sys.path.append('.\\Python\\customTools')

try:
    import create_users  # Importing the file that creates a user matrix
    enabled.append(1)
except ImportError:
    pass

"""
    ---===== Project Manager =====---

    This is an in-house solution to a 
    lack of software. This proprietary
    program is meant to help solve the
    need for managing, creating info,
    creating notes to, and developing
    projects.
    
    - Please do not modify.
    - Please do not claim as [yours].
    - Usage of program does not
      guarantee development.
    - Any damage this may cause is not
      intended. Modification of program
      without authorization does not
      guarantee stability nor does will
      I be held liable for any damage
      that is caused as a result,
      if any.
    
    Content added to this particular
    project at this time is used for
    testing and example.

    Projects will be listed with
    location, name, date uploaded and
    updated. Notes will be editable
    and readable. 
    
    Proprietary @ Jeffrey Miller 2018
    
    If you wish to use this program
    please contact Jeff Miller at one
    of the following locations:
    - 248-705-5198
    - http://www.Jeff3DAnimation.com/
    - Jeff3DAnimation@yahoo.com
"""


class PyPmWnd(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        Run and build our main window

        :param parent: Parent of the widget if there is one
        """

        super(PyPmWnd, self).__init__(parent)
        _doc = './projects.json'
        # Create a menubar
        self.menubar = QtGui.QMenuBar()
        self.setMenuBar(self.menubar)
        self.widget = TopWidget(_doc, self)
        self.build()

    def build(self):
        """
        Build the menu and widget window

        :return:
        """

        # Building menu
        _file = QtGui.QMenu('&File')
        _file.setWindowTitle('File')
        if 0 in enabled:
            _file.addAction('Create &User file', create_users.main)
        if 1 in enabled:
            _file.addAction('Create &Work Dir file', bewdl.main)
        label1 = _file.addAction('Program Based --------')
        _file.addAction('&Copy Project Folder', self.widget.transfer)
        _file.addAction('&Open Master Maya Directory', self.widget.mmdirectory)
        label2 = _file.addAction('Program Based --------')

        # If the thumb-drive exists, list it
        if os.path.isdir('F:\\'):
            _file.addAction('Backup to &F', self.widget.f_)

        _file.addAction('&Backup', self.widget.backup)
        _file.addAction('&Delete', self.widget.delete)
        _file.addAction('&Save', self.widget.gather_and_save)
        label3 = _file.addAction('Maya Based --------')
        _file.addAction('Update &Material Library', self.update_library)
        _file.addAction('&Exit', sys.exit)

        self.setCentralWidget(self.widget.build())
        self.setWindowTitle("Version Controller v.{}".format(
            __version__.__version__
        ))

        _push = QtGui.QMenu('&Push Update')
        _push.setWindowTitle('Push Update')
        _push.addAction('Compile &And Copy', self.widget.compile_transfer)
        _push.addAction('&Push VGC Update', self.widget.comp_copy_vgc)

        self.menubar.addMenu(_file)
        self.menubar.addMenu(_push)

        # Set tearable menu and disable click-able on menu names
        _file.setTearOffEnabled(True)
        _push.setTearOffEnabled(True)
        label1.setEnabled(False)
        label2.setEnabled(False)
        label3.setEnabled(False)

        # Set our menu style for selections
        _file.setStyleSheet(
            'QMenu::item:selected {padding: 2px 30px;}'
            'QMenu::item:!selected {padding: 2px 30px;}'
            'QMenu::item:disabled:selected {background: transparent;}'
            'QMenu::item:enabled:selected {background: #AFDAFF;}'
        )

    def closeEvent(self, event):
        """
        Close event specified by closing the actual window. If the window closes
        catch the event and then gather all information in the table and save.

        :param event:
        :return:
        """

        self.widget.gather_and_save()
        event.accept()

    @staticmethod
    def update_library():
        """
        Launch the material updater tool.

        :return:
        """

        subprocess.Popen(
            [
                "C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\mayapy.exe",
                '{}{}'.format(
                    '.\\Python\\customTools',
                    '\\maya_material_pusher.pyc'
                )
            ],
            shell=True
        )


class TopWidget(QtGui.QWidget):
    def __init__(self, _json_document=str(), parent=None):
        """
        Python Project Manager Window
        Build our GUI.

        :param parent:
        """

        super(TopWidget, self).__init__(parent)
        self.project_doc = _json_document

        # Pre-load all
        _info = jsonReader.main()
        self.da_info = _info.keys()
        self.da_info.sort()
        self.da_dict = _info

        # Window Settings
        self.parent = parent
        # Area to display our project and programs lists
        self.tree_view1 = QtGui.QTreeView()
        self.menu = QtGui.QMenu(self)
        self.model = QtGui.QStandardItemModel()
        # Area to add notes about selected project
        self.notes = Text(self)
        self.notesLbl = QtGui.QLabel("Change Log:")
        self.curNameP = QtGui.QLabel()
        self.curVersP = QtGui.QLabel()
        self.curDateP = QtGui.QLabel()
        self.curNumFP = QtGui.QLabel()
        self.curNumVP = QtGui.QLabel()
        self.nameProj = QtGui.QLabel("Program Name\t:")
        self.versProj = QtGui.QLabel("Program Version\t:")
        self.dateProj = QtGui.QLabel("Program Date\t:")
        self.numFProj = QtGui.QLabel("Num of Files\t:")
        self.numVProj = QtGui.QLabel("Num of Versions\t:")
        self.delName1 = QtGui.QPushButton("Del")
        self.bkupBtn1 = QtGui.QPushButton("Backup")
        self.addButn1 = QtGui.QPushButton("Add Entry")
        self.sbmtBtn1 = QtGui.QPushButton("Save File")
        self.setMinimumSize(750, 400)

    def build(self):
        """
        Assemble the windows UI elements so that it creates a visually appealing
        software for myself and any future programmers.

        :return:
        """

        # Build our layout widgets
        _gridLay1 = QtGui.QGridLayout()
        _gridLay2 = QtGui.QGridLayout()
        _hBoxLay1 = QtGui.QHBoxLayout()
        _hBoxLay2 = QtGui.QHBoxLayout()
        _vBoxLay1 = QtGui.QVBoxLayout()

        # Settings for Tree View
        self.tree_view1.setSortingEnabled(True)
        self.tree_view1.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tree_view1.setModel(self.model)
        self.tree_view1.setUniformRowHeights(True)

        # Setting labels and width for context menu
        _width = 100
        _col1 = "Prog Name"
        _col2 = "Date Crtd"
        _col3 = "Date Upld"
        _col4 = "Prog Vers"

        self.menu.addAction('Delete', self.delete)
        self.menu.addAction('Backup', self.backup)
        self.menu.addAction('Compile And Copy', self.compile_transfer)

        # Commands
        self.addButn1.clicked.connect(PyPmAdd(self).show)
        self.tree_view1.doubleClicked.connect(self.open_folder)
        self.tree_view1.clicked.connect(self.update_file_info)
        self.sbmtBtn1.clicked.connect(self.gather_and_save)
        self.bkupBtn1.clicked.connect(self.backup)
        self.delName1.clicked.connect(self.delete)

        # Set up the grid layout
        _gridLay2.addWidget(self.nameProj, 0, 0)
        _gridLay2.addWidget(self.versProj, 1, 0)
        _gridLay2.addWidget(self.dateProj, 2, 0)
        _gridLay2.addWidget(self.numFProj, 3, 0)
        _gridLay2.addWidget(self.numVProj, 4, 0)
        _gridLay2.addWidget(self.curNameP, 0, 1)
        _gridLay2.addWidget(self.curVersP, 1, 1)
        _gridLay2.addWidget(self.curDateP, 2, 1)
        _gridLay2.addWidget(self.curNumFP, 3, 1)
        _gridLay2.addWidget(self.curNumVP, 4, 1)

        # Set up the horizontal and vertical layouts
        _hBoxLay2.addWidget(self.notesLbl)
        _hBoxLay2.addWidget(self.addButn1)
        _vBoxLay1.addLayout(_hBoxLay2)
        _vBoxLay1.addWidget(self.notes)
        _vBoxLay1.addLayout(_gridLay2)
        _hBoxLay1.addWidget(self.bkupBtn1)
        _hBoxLay1.addWidget(self.delName1)

        # Set up the last grid
        _gridLay1.addWidget(self.tree_view1, 0, 0)
        _gridLay1.addLayout(_vBoxLay1, 0, 1)
        _gridLay1.addLayout(_hBoxLay1, 1, 0)
        _gridLay1.addWidget(self.sbmtBtn1, 1, 1)

        # Bind it to the widget
        self.setLayout(_gridLay1)

        # Custom context menu
        self.tree_view1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_view1.connect(
            self.tree_view1,
            QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
            self.right_click_menu
        )
        # Fix the headers of grid 1
        self.reload(_col1, _col2, _col3, _col4, _width)

        # Add information for each row
        for _eachrow in self.da_info:
            if len(self.da_dict[_eachrow]) > 0:
                _combo = [
                    self.da_dict[_eachrow]['name'][0],
                    self.da_dict[_eachrow]['created'][0],
                    self.da_dict[_eachrow]['uploaded'][0],
                    self.da_dict[_eachrow]['version'][0],
                    self.da_dict[_eachrow]['location'][0]
                ]

                PyPmAdd(self, _combo)

        return self

    def f_(self, _whichone=str()):
        """
        Back up information to our F: Drive, a thumb-drive. Constant across
        all computers.

        :param _whichone: 'all', '' / some other information provides
                          functionality based on which directory to be zipped
                          up, backed up and / or transferred.
        :return:
        """

        if _whichone == 'all':
            _info = self.zip('.\\project_folder')
        else:
            _info = self.backup()

        if _info is not '':
           shutil.move(_info, 'F:\\')

    def comp_copy_vgc(self):
        """
        Compile and copy the most up-to-date configurator project and deploy it
        in the proper location(s).

        :return:
        """

        # Create an empty dictionary to set our compiled informationt to.
        _compiled_list = dict()
        _dir = '.\\project_folder\\config_json\\archive'
        _files = os.listdir(_dir)

        # Get an array of files that do not contain '.' / an extension
        _list = [x for x in _files if '.' not in x]
        for _each in _list:
            # Get the version of each file
            _main = int(_each.split('v')[1])
            _compiled_list.setdefault(_main, _each)

        # Get the max version of each file
        _get_newest = max(_compiled_list.keys())
        _newest = _compiled_list[_get_newest]

        # Get the files ending with .py
        for _file in os.listdir(_dir + '\\' + _newest):
            if _file.endswith('.py'):
                # Send them to the compiler
                self.compiler(_file, _dir + '\\')

        # Set two empty arrays so we can designate where files go
        _py = list()
        _pyc = list()
        _all = os.listdir(_dir + '\\' + _newest)
        for _every_file in _all:
            # If it ends with pyc / is compiled
            if _every_file.endswith('.pyc'):
                _pyc.append(_every_file)

            # If it ends with py / source
            elif _every_file.endswith('.py'):
                _py.append(_every_file)

        user = '.\\Python\\config'
        for _every_pyc in _pyc:
            # Copy our compiled files to this location (used in-house)
            shutil.copy(_dir + '\\' + _every_pyc, user + '\\' + _every_pyc)

        client = '.\\Python27\\Lib\\config'
        for _every_py in _py:
            # Copy our compiled files to this loc (embedded in maya / source)
            shutil.copy(_dir + '\\' + _every_py, client + '\\' + _every_py)

        print 'Finished pushing the update to the config version: {}!'.format(
            _get_newest
        )

    @staticmethod
    def compiler(_compile_this=None, _directory=str()):
        """
        The method created for easily compiling an array of listed file(s).

        :param _compile_this: Compile the array or file (list() / str())
        :param _directory: In this location
        :return:
        """

        # Run the compiler
        pyc.compile(_directory + _compile_this)

        # create an array of compiled files
        _compiled = list()
        for _every_file in os.listdir(_directory):
            if _every_file.endswith('.pyc'):
                _compiled.append(_directory + _every_file)

        # Return so we can transfer or print them.
        return _compiled

    def compile_transfer(self):
        """
        Compile the selected rows file and transfer it to the correct directory

        :return:
        """

        row = self.tree_view1.selectionModel().currentIndex().row()
        _item = self.model.item(row, 0)
        _name = _item.text()
        _itTT = _item.toolTip().split(":\t")[-1:]
        _text = _itTT[0]

        # Title: location for specified items
        _key_watchout = {
            'customTools': '.\\project\\customTools',
            'Modules': '.\\direct\\Modules'
        }

        # create an array of python files to compile
        _compile_these = list()
        if _name.endswith('.py'):
            _dir = _text
            _compile_these.append(_dir + _name)

        else:
            # If not a list, get the name of the file
            _dir = _text + _name
            for _each in os.listdir(_dir):
                if _each.endswith('.py'):
                    _compile_these.append(_dir + _each)

        # Compile the list and receive the array
        _compiled = list()
        for _each_script in _compile_these:
            _compiled.append(self.compiler(_each_script, _dir))

        _dire = _dir.split('\\')[-1:][0]
        for _key in _key_watchout.keys():
            if _key in _dire:
                _dire = _key_watchout[_dire]
            else:
                _dire = ''

        _v_dir = '.\\Python\\{}{}'.format(
            _dire, _name + 'c'
        )

        # Move the files to the correct location
        for _each_file in _compiled:
            shutil.move(_each_file, _v_dir)

        print 'Finished'

    @staticmethod
    def mmdirectory():
        # Open the directory to the material library
        os.startfile('.\\MasterMaya')

    @staticmethod
    def transfer():
        """
        Transfer the files from local to isolated

        :return:
        """

        print 'Removing the Drive Project Folder.'
        shutil.rmtree('C:\\project_folder')
        print 'Beginning copying.'
        shutil.copytree('.\\project_folder', 'C:\\project_folder')
        print 'Finished copying.'

    def reload(self, _col1, _col2, _col3, _col4, _width):
        """
        Reload the headers so that they appear appropriately.

        :param _col1: First column item
        :param _col2: Second column item
        :param _col3: Third column item
        :param _col4: Fourth column item
        :param _width: Width of each item
        :return:
        """

        # Clear the headers
        self.model.clear()

        # Re-add the headers
        self.model.setHorizontalHeaderLabels([_col1, _col2, _col3, _col4])

        # Set their widths
        self.tree_view1.setColumnWidth(0, (_width + 50))
        self.tree_view1.setColumnWidth(1, (_width - 30))
        self.tree_view1.setColumnWidth(2, (_width - 30))
        self.tree_view1.setColumnWidth(3, (_width - 50))

    def attain_gui_element(self):
        """
        Attain the gui elements.

        :return:
        """

        # Attain the model
        _model = self.model
        return _model

    def open_folder(self):
        """
        Double-clicked item will attain the location in the tool tip and
        open the folder up in windows.

        :return:
        """

        # Open the directory in a new explorer window and select the item
        _item = self.tree_view1.selectedIndexes()
        _item = self.model.itemFromIndex(_item[0])
        _row = self.tree_view1.selectionModel().currentIndex().row()
        _folder = self.model.item(_row, 0).text()
        _itTT = _item.toolTip().split(":\t")[-1:][0] + str(_folder)

        # We have created the tool tip item
        subprocess.Popen('explorer /select, {}'.format(_itTT))

    def update_file_info(self):
        """
        Update the selection.

        :return:
        """

        # Clear the notes widget
        self.notes.clear()

        # Get the notes information from the json document.
        _info = jsonReader.main()
        _keys = _info.keys()
        _keys.sort()

        # Get the selected index
        _slIt = self.tree_view1.selectedIndexes()
        ra = range(0, 4)
        # Set the tool tip for each item in the row
        _m_ind = [self.model.itemFromIndex(_slIt[i]) for i in ra]
        _project_name = _m_ind[0].text()

        # Get the current row and get the notes, then set it
        row = self.tree_view1.selectionModel().currentIndex().row()
        _header = self.model.item(row, 0).text()
        _notes = _info[_header]['notes'][0]

        # Get the main directory
        _main_directory = _m_ind[0].toolTip().split(":\t")[-1:][0]
        if _main_directory.endswith('\\\\'):
            _main_directory = _main_directory[:-2]
        elif _main_directory.endswith('\\'):
            _main_directory = _main_directory[:-1]
        # Format the directory and project name
        _project_loc = '{}\\{}'.format(
            _main_directory,
            _project_name
        )

        # Set the tool tips information after we have attained all we need
        _itm1 = self.model.itemFromIndex(_slIt[0]).text()
        _split = _itm1.split('_')[:-1]
        _tooltip = (
            self.model.itemFromIndex(_slIt[0]).toolTip().split(":\t")[-1:][0]
        )
        _proj_loc = '{}{}'.format(
            _tooltip.replace('\\\\', '\\'),
            _itm1
        )
        if '.' not in _project_loc:
            _project_info = len(os.listdir(_proj_loc))
        else:
            _project_info = 1
        _itm3 = self.model.itemFromIndex(_slIt[2]).text()
        _itm4 = self.model.itemFromIndex(_slIt[3]).text()

        # setting it all
        self.curNameP.setText(str(_itm1))
        self.curVersP.setText(str(_itm4))
        self.curDateP.setText(str(_itm3))
        self.curNumFP.setText(str(_project_info))
        self.curNumVP.setText(str(len(
            [x for x in os.listdir(_tooltip) if '_'.join(_split) in x]
        )))

        # Officially setting the notes
        self.notes.setText(_notes)

    def gather_and_save(self):
        """
        Gather all items in the QTreeView and allocate them into a dictionary
        then save it out as a json document. All items are part of a model.
        The model will be the item that contains the information. Grab the
        model items row and column and attain the text associated with it.

        :return:
        """

        # Get the json documents matrix
        _temp = jsonReader.main()

        # Get the data
        data = {}
        for row in range(self.model.rowCount()):
            # Attain the items text
            _header = self.model.item(row, 0).text()
            for column in range(8):
                if column == 0:
                    obj = "name"
                    _text = self.model.item(row, column).text()

                elif column == 1:
                    obj = "created"
                    _text = self.model.item(row, column).text()

                elif column == 2:
                    obj = "uploaded"
                    _text = self.model.item(row, column).text()

                elif column == 3:
                    obj = "version"
                    _text = self.model.item(row, column).text()

                elif column == 4:
                    obj = "location"
                    _item = self.model.item(row)
                    _itTT = _item.toolTip().split(":\t")[-1:]
                    _text = _itTT[0]

                elif column == 5:
                    obj = "numVer"
                    _text = self.curNumFP.text()

                elif column == 6:
                    obj = "numPro"
                    _text = self.curNumVP.text()
                    self.tree_view1.clearSelection()

                elif column == 7:
                    obj = 'notes'
                    try:
                        _text = _temp[_header]['notes'][0]
                    except KeyError:
                        _text = self.notes.toPlainText()
                    self.notes.clear()

                else:
                    obj = str()
                    _text = str()

                # Apply it all to the data matrix
                data.setdefault(_header, {}).setdefault(obj, []).append(_text)

        # Write that matrix out!!!
        jsonWriter.JsonWriter(data)

    def right_click_menu(self, q_pos=None):
        """
        Create a right click menu or custom context menu.

        :param q_pos: The QPoint Location of our mouse
        :return:
        """
        # Custom context menu
        _parent_pos = self.tree_view1.mapToGlobal(QtCore.QPoint(0, 0))
        _item = self.tree_view1.indexAt(q_pos).row()
        if _item > -1:
            # Move it to where our pointer is and show it
            self.menu.move(_parent_pos + q_pos + QtCore.QPoint(0, 25))
            self.menu.show()

    @staticmethod
    def zip(_location=str()):
        """
        Zip the location specified and return the information

        :param _location: string regarding our specified location.
        :return:
        """
        # Execute our zipping of a directory or file
        _zip = ['C:\\Program Files\\7-Zip\\7z.exe']
        _zip_flags = [
            'a',
            '-y',
            '-m0=lzma2:d1024m',
            '-mx9',
            '-aoa',
            '-mfb=64',
            '-md=32m',
            '-ms=on',
        ]
        rc = subprocess.Popen(
            _zip + _zip_flags + [
                _location + '.7z',
                _location
            ]
        )

        # Wait til the process is done
        rc.wait()
        # Retrun that information
        return '{}.7z'.format(_location)

    def backup(self):
        """
        Backup selected entry.

        :return:
        """

        # Get the selected indexes row.
        row = self.tree_view1.selectionModel().currentIndex().row()
        _item = self.model.item(row, 0)
        # Get the items tool tip information, like its location
        if _item is not None:
            _name = _item.text()
            _itTT = _item.toolTip().split(":\t")[-1:]
            _location = _itTT[0]
            # Create the string needed to send our file or directory to the zip
            _backup_this = _location + _name

            # Return our zip information
            return self.zip(_backup_this)

    def delete(self):
        """
        Delete entry.

        :return:
        """

        # Delete the selected index / clear it from the qtreeview
        _item = self.tree_view1.selectedIndexes()
        self.tree_view1.model().takeRow(_item[0].row())
        # Clear the notes
        self.notes.clear()
        # Save the information into the json document / remove the item
        self.gather_and_save()


class Text(QtGui.QTextEdit):
    """
    Text

    :param parent:
    """

    def __init__(self, parent=None):
        """
        Create a text edit that allows to, minimally, add a description to our
        current selected item in the qtreeview. This is essentially allowing
        us to create a bug or change log for whatever queried object we have
        added.

        :param parent: Parent to this widget
        """

        super(Text, self).__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        """
        Get the key press event

        :param event: What keyboard key was pressed?
        :return:
        """

        # If return is pressed, we want to save the information
        if event.key() == QtCore.Qt.Key_Return:
            self.save_it_out()
        # If backspace pressed, remove the last item
        elif event.key() == QtCore.Qt.Key_Backspace:
            _text = self.toPlainText()
            self.setText(_text[:-1])
        # If delete pressed, clear the entire text edit
        elif event.key() == QtCore.Qt.Key_Delete:
            self.clear()
        else:
            # Otherwise, append our information on the end of current typed
            _text = self.toPlainText()
            self.setText((_text + event.text()).replace('\n', ''))

    def save_it_out(self):
        """
        Save the information to the json document / update the info.

        :return:
        """

        # Read the json document
        _temp_info = jsonReader.main()
        _each = 0

        # If we match our selection to the key in the json document
        while _each < self.parent.model.rowCount():
            _header = self.parent.model.item(_each, 0).text()
            if (
                    _each ==
                    self.parent.tree_view1.selectionModel().currentIndex().row()
            ):
                # Get the text and clear it
                _text = self.toPlainText()
                self.clear()
                try:
                    # Delete the key if it exists
                    del _temp_info[_header]['notes']
                except KeyError:
                    pass

                # Add the new key with the information we got as an array
                _temp_info[_header].setdefault('notes', [_text])

            else:
                # Otherwise add the information
                _text = _temp_info[_header]['notes']
                try:
                    del _temp_info[_header]['notes']
                except KeyError:
                    pass

                # Add the new key with the information we got as a string
                _temp_info[_header].setdefault('notes', _text)

            _each += 1

        # Save that json document out!!!
        jsonWriter.JsonWriter(_temp_info)


class PyPmAdd(QtGui.QDialog):
    def __init__(self, parent=None, _pass_with_info=list()):
        """
        Add an entry into the QTreeView.

        :param parent:
        """

        super(PyPmAdd, self).__init__(parent)
        self.editMe = parent

        if _pass_with_info != list():
            self.add_to_list(_pass_with_info)

        else:
            self.nF1 = PyPmLine(self)
            self.nF2 = PyPmLine(self)

            # Window Settings
            self.setWindowTitle("Add Build")
            self.setModal(False)
            self.setAcceptDrops(True)

            # Start Program
            self.add_window()

    def add_window(self):
        """
        Create the add window

        :return:
        """

        # Widgets
        _gridLay1 = QtGui.QGridLayout()
        _tagName1 = QtGui.QLabel("Prog Name")

        _tagName2 = QtGui.QLabel("Prog Link")

        _addName1 = QtGui.QPushButton("Add to List")
        _closeBtn = QtGui.QPushButton("Close")

        # Commands
        _addName1.clicked.connect(self.add_to_list)
        _closeBtn.clicked.connect(self.close)

        # Marking Layouts
        _gridLay1.addWidget(_tagName1, 0, 0)
        _gridLay1.addWidget(self.nF1, 0, 1)
        _gridLay1.addWidget(_tagName2, 1, 0)
        _gridLay1.addWidget(self.nF2, 1, 1)
        _gridLay1.addWidget(_addName1, 0, 2)
        _gridLay1.addWidget(_closeBtn, 1, 2)

        self.setLayout(_gridLay1)

    def add_to_list(self, _info=None):
        """
        Add the project file and directory to the qtreeview. Info, if we have
        any, will be added.

        :param _info: If info exists in list form, we will use it
        :return:
        """

        # Get the model
        _model = self.editMe.attain_gui_element()

        if _info == list():
            _combo = [
                str(_info[0]),
                str(_info[1]),
                str(_info[2]),
                str(_info[3]),
                str(_info[4]),
            ]

        else:
            # File Name and Location
            _nameField0 = self.nF1.text()
            # _nameField1 = self.nF1.text().split(".")[0]
            _nameField2 = self.nF2.text()

            # Todays MONTH, DAY, YEAR
            _today = str(datetime.date.today()).split("-")
            _today = "-".join([_today[1], _today[2], _today[0]])

            _cDate = os.path.getctime(_nameField2 + "\\" + _nameField0)
            _cDate = datetime.datetime.fromtimestamp(_cDate).strftime(
                '%m-%d-%Y'
            )
            _cDate = str(_cDate)

            # Add the combo
            _combo = [
                str(_nameField0),
                str(_cDate),
                str(_today),
                str('1.0.0'),
                str(_nameField2)]

        _row = _model.rowCount()

        i = 0
        while i < (len(_combo) - 1):
            # Add a qstandarditem to the qtreeview
            _item = QtGui.QStandardItem(_combo[i])
            # Not editable!!!!!
            _item.setEditable(False)
            _model.setItem(_row, i, _item)

            # Add a tooltip to that item
            _item.setToolTip(
                "File name\t:\t" + _combo[0] + "\n" +
                "File date\t:\t" + _combo[1] + "\n" +
                "File user\t:\t" + _combo[2] + "\n" +
                "File size\t:\t" + _combo[3] + "\n" +
                "File location\t:\t" + _combo[4]
            )

            i += 1

        if _info == list():
            # Save the information!!!!
            self.editMe.gather_and_save()
        # print(_today, "\n", _nameField1, "\n", _nameField2)

    def dragEnterEvent(self, event):
        """
        Get the drag event

        :param event: Passed event
        :return:
        """

        # Get the dragged in information and copy the data locally
        _data = event.mimeData()
        # Get the uniform resource locator
        if _data.hasUrls():
            # We have it
            if len(_data.urls()) == 1:
                _fixThis = str(_data.urls()[0])
                _spltted = _fixThis.split("///")[1].replace("')", "")
                _fileNam = _spltted.split("/")[-1:][0]
                _filePat = "\\".join(_spltted.split("/")[:-1]) + '\\'

                # Add that information into the individual text boxes
                self.nF1.setText(_fileNam)
                self.nF2.setText(_filePat)


class PyPmLine(QtGui.QLineEdit):
    def __init__(self, parent=None):
        """
        QlineEdit for receiving information. We may add more to this later

        :param parent: Parent of the widget
        """

        super(PyPmLine, self).__init__(parent)
        self.setDragEnabled(False)


def main():
    _window_to_show = PyPmWnd()
    _window_to_show.show()
    return _window_to_show


if __name__ == "__main__":

    try:
        app = QtGui.QApplication(sys.argv).instance()

    except RuntimeError:
        app = QtGui.QApplication.instance()

    window = main()
    sys.exit(app.exec_())
