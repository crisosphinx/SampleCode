#!/usr/bin/python
# -*- coding: utf-8 -*-

import maya.cmds as cm
from time import time


class ExtremeProgressWnd:
    def __init__(
            self,
            start,
            end=None,
            step=1,
            strng=str(),
            order=list()
    ):
        """
        Special Progress Bar with text next to it displaying
        progress and information pertaining to completion.

        :param start: Start amount (usually zero)
        :param end: End amount (max number of objects)
        :param step: Amount to step by
        """

        if end is None:
            self.start = 0
            self.end = start
        else:
            self.start = start
            self.end = end

        self.step = step
        self.text_to_display = strng
        self.main_list = order

        try:
            ExtremeProgressWnd(
                self.start,
                self.end,
                self.step,
                self.text_to_display
            ).setup()
        except:
            pass

    @staticmethod
    def __doc__():
        doc = \
            """
        This program boots a window with a progress bar attached to it
        and with multiple text entries specified on it depicting:
          -  percentage completed
          -  current/total completed
          -  estimated time
          -  elapsed time
        """

        return doc

    @staticmethod
    def __version__():
        return "1.0.0"

    def __iter__(self):
        self.start_time = time()
        self.current = self.start
        return self

    def next(self):
        if self.current >= self.end:
            ExtremeProgressWnd(
                self.start,
                self.end,
                self.step,
                self.text_to_display
            ).end_pw()
            raise StopIteration

        sta = self.start
        self.current += self.step
        _perc = ExtremeProgressWnd(
                    self.current,
                    self.end,
                    self.step,
                    self.text_to_display
                ).percentage(self.current-self.step, sta)

        _prct = _perc[1]
        _elapsed = time() - self.start_time

        if _elapsed > 60.0:
            _elapse = "{} {}".format(
                round(
                    float((_elapsed + 0.0) / 60.0), 2),
                "mins"
            )
        else:
            _elapse = "{} {}".format(round(_elapsed, 2), "secs")

        try:
            estimate = float(
                _elapsed / (_perc[0] - _elapsed)
            )
            if estimate > 60.0:
                _estleft = "{} {}".format(round(
                    float((estimate + 0.0) / 60.0), 2),
                    "mins"
                    )
            else:
                _estleft = "{} {}".format(round(estimate, 2), "secs")
        except:
            _estleft = 0

        cm.progressWindow(
            e=1,
            step=self.step,
            status="""
            {disp}: {perc}%
            {elps}: {etim}
            {left}: {ltim}
            {comp}: {cur}/{end}
            {item}: {item_list}
            """.format(
                disp="% Completed\t", perc=_prct,
                elps="Elapsed\t\t", etim=_elapse,
                left="Time Left\t", ltim=_estleft,
                comp="Completed\t", cur=self.current, end=self.end,
                item="Processing\t", item_list=self.main_list[self.current-1],
                n=2,
                ii=1,
            ),
        )

        return self.current - self.step

    def setup(self):
        cm.progressWindow(
            title=self.text_to_display,
            min=self.start,
            max=self.end,
            status="""
            {disp}: {perc}%
            {elps}: {etim}
            {left}: {ltim}
            {comp}: {cur}/{end}
            """.format(
                disp="% Completed\t", perc=0,
                elps="Elapsed\t\t", etim=0.00,
                left="Time Left\t", ltim="-",
                comp="Completed\t", cur=0, end=self.end,
                n=2,
                ii=1,
            ),
            pr=0,
        )

    @staticmethod
    def end_pw():
        cm.progressWindow(
            ep=1,
        )

    def percentage(self, curnt, start):
        cur = float(curnt + 0.0)
        sta = float(start + 0.0)
        end = float(self.end + 0.0)
        _fraction = float((cur + 1) / (end - sta))
        _percent = round((_fraction * 100), 2)
        return _fraction, _percent
