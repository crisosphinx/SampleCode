import json


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


class JsonWriter:
    def __init__(self, _passed_info=dict()):
        """
        Get the passed information and designate the two locations the file
        will be placed. Should be on the server and a local directory copy.

        :param _passed_info: JSON dictionary to dump.
        """

        self.data = _passed_info
        self.doc_loc = (
            '.\\Documentations'
        )
        self.project = '.\\project.json'
        self.write_json()
        
    def write_json(self):
        """
        Load a JSON file, read and return it

        :return:
        """
        
        _data = self.data
        with open(self.project, "w") as _outfile:
            if (
                    _data is not None and
                    _data != "" and
                    _data != {} and
                    len(_data) is not 0
            ):
                json.dump(_data, _outfile)
                print 'Saved local copy.'

        with open((self.doc_loc + "\\project.json"), "w") as _outfile:
            if (
                    _data is not None and
                    _data != "" and
                    _data != {} and
                    len(_data) is not 0
            ):
                json.dump(_data, _outfile)
                print 'Saved server copy.'
                return 1
            
            else:
                return 0
