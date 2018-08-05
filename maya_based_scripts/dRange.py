class Range:
    def __init__(self, start=float(), stop=float(), step=float()):
        """
        Class creates a text based decimal range.

        :param start: Start float
        :param stop: End float
        :param step: The Step we take through the range
        """

        self.start = start
        self.stop = stop
        self.step = step

    @staticmethod
    def __doc__():
        doc = \
            """
        Programmed by Jeff Miller 2017
        Jeff3DAnimation@yahoo.com
        Jeff3DAnimation.com

        This tool creates an array containing strings to be interpreted as
        floats. The string can be added as a piece of text for a button.
        """

        return doc

    def decimal(self):
        """
        Get our decimals and return the information

        :return:
        """

        while self.start <= (self.stop + self.step):
            yield self.start
            self.start += self.step


def main(start, stop, step):
    # We have a generator, now get the string based floats
    _generator = Range(start, stop, step).decimal()
    _retrn_arr = ['{0:.3f}'.format(float(x)) for x in _generator]

    # Return our array
    return _retrn_arr
