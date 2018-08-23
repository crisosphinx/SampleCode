import json
import os

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


class JsonReader:
    def __init__(self):
        self.doc_loc = (
            'V:\\VG_Project_Management\\' +
            'VGProgramming_Documentation\\Documentations'
        )
        self.project = './project.json'
        
    def load_json(self):
        """
        Load a JSON file, read and return it.

        :return:
        """

        if os.path.isfile(self.doc_loc) or os.path.isfile(self.project):
            if os.path.isfile(self.doc_loc):
                _file_to_load = self.doc_loc

            else:
                _file_to_load = self.project

            with open(_file_to_load, "r") as _infile:
                _jsonFile = json.load(_infile)
                return _jsonFile

        else:
            return {}


def main():
    return JsonReader().load_json()
