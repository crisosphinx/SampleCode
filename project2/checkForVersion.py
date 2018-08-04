import os

"""
    ---===== Project Manager =====---
    
    This is an in-house solution to a 
    lack of software. This proprietary
    program is meant to help solve the
    need for managing, creating info,
    creating notes to, and developing
    projects.
    
    Projects will be listed with
    location, name, date uploaded and
    updated. Notes will be editable
    and readable. 
    
"""


class FileParser:
    def __init__(self, directory=None):
        """
        File parser looks for the amount of file versions for any particular
        project or looks for the __version__ file. __version__ file will return
        the version of the project.

        :param directory:
        """

        self.dir = directory
        self.dirArray = os.listdir(self.dir)
    
    def dir_ver_dectector(self):
        """
        Detect which version is running.

        :return: 
        """
        
        if "__version__.py" in self.dirArray:
            # Found the file version, opening to attain value
            _file_open = open(self.dir + "\\__version__.py", "r")
            opened = _file_open.read()
            for each in opened:
                if "__version__" in each.lower():
                    # Got value, returning
                    _split = each.split("=")[1].replace(" ", "")
                    return _split
        
        else:
            # Could not find the __version__ file, getting amount of files
            return self.file_ver_detector()
        
    def file_ver_detector(self):
        """
        Detect how many file versions there are.

        :return:
        """

        _versions = [x for x in self.dirArray if "_v" in x]

        # If there are no files that have "_v" in it, get the amount
        if len(_versions) == 0:
            _versions = [x for x in self.dirArray if "_v" not in x]
            _versions = _versions.sort().reverse()

        # Get the max one
        _max_ver = _versions[0]

        # Open that file
        _file_open = open(_max_ver, "r")
        opened = _file_open.read()
        
        for each in opened:
            # Find the version
            if "ver" in each.lower():
                _split = each.split("=")[1].replace(" ", "")
                return _split
            
            else:
                # Not there, return 1.0.0, first version available
                return "1.0.0"
        
    def amount_file_detector(self):
        """
        Detect which file is available.

        :return:
        """

        _ver_files = []
        # Get the files in the directory
        _all_files = os.listdir(self.dir)
        for eachFile in _all_files:
            # Found __version__
            if "__version__" in eachFile:
                for dir, dirname, filename in os.walk(self.dir):
                    _ver_files.append(dirname)

            # found _v000 version
            elif "_v" in eachFile:
                _ver_files.append(eachFile)

        # Return the amount we found
        return str(len(_ver_files))
