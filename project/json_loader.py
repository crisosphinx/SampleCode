import os
import json


class DTJson:
    def __init__(self, load=bool(), _file=str(), content=None):
        """
        This script either creates or loads a json document for the
        Dungeon Tracker.

        :param load: Boolean for loading or saving the file.
        :param _file: The file location.
        :param content: The content to be saved to the file.
        """

        self.file = _file
        self.load = load
        self.content = content

    def writer(self):
        """
        Alert the user that the file has been saved and dump the matrix into
        the JSON document.

        :return:
        """

        print('-== SAVED ==-')

        _file = self.file
        with open(_file, 'w') as f:
            json.dump(self.content, f)
            f.close()

        return 'Finished'

    def loader(self):
        """
        Method loads the specified json file. If it does not load, it creates
        one and then loads it.

        :return:
        """

        print('-== LOADED ==-')
        # Get the file name
        filename = self.file

        # Check to see if it exists and ends with .json then load it
        if os.path.isfile(filename):
            if filename.endswith('.json'):
                with open(filename, 'r') as f:
                    # Load and return the content
                    content = json.load(f)
                    # Free our memory up, even if just a little
                    f.close()
                    return content

        else:
            # If the file does not exist, create one and then load it
            main(load=False, _file=filename, content={})
            return main(load=True, _file=filename)


def main(load=bool(), _file=str(), content=dict()):
    """
    This method runs the main application based on the flags specified.

    :param load: Boolean for if we want to load or save the file.
    :param _file: Passed string; specifies the file name
    :param content: Pass the matrix to embed in the json document.
    :return:
    """

    if load is False:
        return DTJson(load, _file, content).writer()

    else:
        return DTJson(load, _file, content).loader()


if __name__ == '__main__':
    """
    Simply running this causes us to just create a file.
    """

    main(load=True)
