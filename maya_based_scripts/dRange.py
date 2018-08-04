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
