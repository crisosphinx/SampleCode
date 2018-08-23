from _winreg import *

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


class ChkBatInstallDir:
    def __init__(self, json=dict()):
        """
        Check the install folders

        :param json:
        """

        # Loads the values from the passed Matrix from the json document
        self.dg_hkey1 = json['dg_hkey1']
        self.dg_hkey2 = json['dg_hkey2']
        self.x64 = json['x64']
        self.ma_hkey = json['ma_hkey']

    def reg_key(self, ver=str()):
        """
        Get REG KEY

        :param ver: Version of program to find; Maya or DG
        :return:
        """

        # REG KEY for Maya
        if ver == "Maya":
            maya_path = self.ma_loc()
            if type(maya_path) == str:
                return str(maya_path) + '\\bin'
            else:
                return maya_path + 'bin'

        # REG KEY for DG
        elif ver == "DG":
            return self.dg_loc()

    @staticmethod
    def test_subkey(*args):
        """
        Test the subkeys, incoming must be a list so we can extract each
        key set.

        :param args:
        :return:
        """

        # Test to see if registry key exists.
        _reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

        for _each in args:
            for _every in _each:
                try:
                    _subkey = OpenKey(
                        _reg,
                        _every,
                        0,
                        KEY_READ | KEY_WOW64_64KEY
                    )

                    return _subkey

                except WindowsError:
                    print('This key:\n\t{}\n\nDoes not exist'.format(_every))
                    pass

    def dg_loc(self):
        """
        Check to see if reg key contains DeltaGen 2018.1 or 12.1

        :return:
        """

        # Location of potential registry key.
        _rtt_deltagen = self.dg_hkey1
        _3de_deltagen = self.dg_hkey2
        _key_to_read1 = "SOFTWARE\\{}\\{}".format(
            self.x64,
            _rtt_deltagen
        )
        _key_to_read2 = "SOFTWARE\\{}\\{}".format(
            self.x64,
            _3de_deltagen
        )

        # Test to see if registry key exists.
        _subkey = self.test_subkey([_key_to_read2, _key_to_read1])
        if _subkey:
            _pathname, _regtype = QueryValueEx(_subkey, "InstallLocation")

            # Get the path directory
            return _pathname

    def ma_loc(self):
        """
        Check to see if reg key contains Maya 2016.5 with

        :return:
        """

        # Location of potential registry key.
        _maya_loc = self.ma_hkey
        _key_to_read = "SOFTWARE\\{}".format(_maya_loc)

        # Test to see if registry key exists.
        _subkey = self.test_subkey([_key_to_read])

        # If the subkey exists
        if _subkey:
            _pathname, _regtype = QueryValueEx(_subkey, "MAYA_INSTALL_LOCATION")
            # Get the path directory
            return _pathname
