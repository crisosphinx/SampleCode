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
    
    Projects will be listed with
    location, name, date uploaded and
    updated. Notes will be editable
    and readable. 
    
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
