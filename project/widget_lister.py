from PySide import QtGui


class WidgetLister:
    def __init__(self, widget=None):
        self.widget = widget

    def get_child_text(self):
        _text_to_return = []
        _child = []
        if type(self.widget) != QtGui.QTextEdit:
            try:
                _amount = self.widget.count()
                i = 0
                while i < _amount:
                    _temp = self.widget.itemAt(i).widget()
                    _child.append(_temp)
                    if type(_temp) == QtGui.QLineEdit:
                        _info = _temp.text()
                        _text_to_return.append(_info)
                    i += 1
            except AttributeError:
                pass

        else:
            _child = self.widget
            _info = _child.toPlainText()
            _text_to_return.append(_info)

        return _text_to_return, _child


def main(widget=None):
    return WidgetLister(widget).get_child_text()
