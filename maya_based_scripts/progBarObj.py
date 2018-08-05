#!/usr/bin/python
# -*- coding: utf-8 -*-

import maya.cmds as cm
from time import time


class ExtremeProgressBar:
    def __init__(
            self,
            start=None,
            end=None,
            step=None,
            parent=None,
            strng=None,
    ):
        """
        Special Progress Bar with text next to it displaying
        progress and information pertaining to completion.

        :param start: Start amount (usually zero)
        :param end: End amount (max number of objects)
        :param step: Amount to step by
        :param parent: Who is it parented to?
        """

        if start is None:
            self.start = 0
            self.end = start
        else:
            self.start = start
            self.end = end

        self.step = step
        self.parent = parent
        self.text_to_display = strng

    @staticmethod
    def __doc__():
        doc = \
            """
        Programmed by Jeff Miller 2018
        Jeff3DAnimation@yahoo.com
        Jeff3DAnimation.com
        
        This tool is a progress bar that sets up as a child object
        to the window that it is parented to. The progress bar is
        an actual progress bar with a few text options that display
        next to it. The items it displays are as follows:
          -  Time Elapsed
          -  Time Left
          -  Completed objects
        """

        return doc

    @staticmethod
    def __version__():
        """
        Return a version

        :return:
        """

        return "1.0.0"

    def __iter__(self):
        """
        Iterate through integers. We have been provided a range of course.

        :return:
        """

        self.start_time = time()
        self.cur = self.start
        return self

    def next(self):
        """
        Part of our iterator.

        :return:
        """

        # Get the next item
        if self.cur != self.end:
            cm.progressBar(
                "extremePBandJ",
                e=1,
                step=self.cur,
                bp=1,
                status=self.text_to_display,
            )

            # Get the percentage to display
            _perc = ExtremeProgressBar(
                    self.cur,
                    self.end,
                    self.step,
                    self.parent,
                    self.text_to_display
                ).percentage(self.cur-self.step, sta)

            # Get the elapsed time
            _elapsed = round(time() - self.start_time, 3)

            # Get the estimated time for finishing the next item
            _estleft = float(
                _elapsed / (_perc - _elapsed)
            )

            # Print the updates in the text controls
            cm.text(
                "timeleft",
                e=1,
                label="\tTime Left : {}\t|\t".format(_estleft)
            )
            cm.text(
                "elapsed",
                e=1,
                label="Elapsed    : {}\t|\t".format(_elapsed)
            )
            cm.text(
                "numleft",
                e=1,
                label="Completed  : {}/{}".format(self.cur+1, self.end)
            )

        # Step tot he next
        self.cur += self.step

        # If we get to more than the end integer, stop
        if self.cur > self.end:
            ExtremeProgressBar().epb_end()
            raise StopIteration

        # Return our current item / integer
        return self.cur

    def epb_run(self):
        """
        Run our "Extreme Progressbar window"

        :return:
        """

        # If it does not equal the end
        if self.cur != self.end:
            cm.progressBar(
                "extremePBandJ",
                e=1,
                pr=self.cur
            )

            # Update the information
            _elapsed = round(time()-self.start_time, 3)
            _estleft = float(
                (self.cur + 0.0)/((self.end+0.0)-(self.start+0.0))
            )

            cm.text(
                "timeleft",
                e=1,
                label="\tTime Left : {}\t|\t".format(_estleft)
            )
            cm.text(
                "elapsed",
                e=1,
                label="Elapsed    : {}\t|\t".format(_elapsed)
            )
            cm.text(
                "numleft",
                e=1,
                label="Completed  : {}/{}".format(self.cur+1, self.end)
            )

        else:
            # We have reached the end, so run the end script
            ExtremeProgressBar().epb_end()

    def epb_setup(self):
        """
        Set up how our print outs will look

        :return:
        """

        cm.rowColumnLayout("extCol", nc=4)
        cm.progressBar(
            "extremePBandJ",
            min=self.start,
            max=self.end,
            p="extCol",
            # s=self.step,
        )

        # Edit our text items
        cm.text(
            "timeleft",
            label="\tTime Left : \t|\t"
        )
        cm.text(
            "elapsed",
            label="Elapsed    : \t|\t"
        )
        cm.text(
            "numleft",
            label="Completed  : "
        )

    def epb_end(self):
        """
        End method for our process window.

        :return:
        """

        cm.progressBar(
            "extremePBandJ",
            e=1,
            ep=1
        )

        cm.text("timeleft", e=1, l="\tTime Left : \t0.000")

    def percentage(self, curnt=int(), start=int()):
        """
        Calculate the percentage left

        :param curnt: Current integer
        :param start: Start integer
        :return:
        """

        cur = float(curnt + 0.0)
        sta = float(start + 0.0)
        end = float(self.end + 0.0)
        _fraction = float(cur / (end - sta))
        _percent = round((_fraction * 100), 2)

        # Return our calculated percentage.
        return _percent
