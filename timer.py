"""
Michael Harrington

This file provides function for timeing
"""

from time import time

def timeStampMS():
    return int(round(time() * 1000))

class TimerMS():
    def __init__(self):
        self.startTime = None
        self.endTime = None

    def __enter__(self):
        self.startTime = timeStampMS()

    def __exit__(self, typ, value, traceback):
        self.endTime = timeStampMS()

    @property
    def time(self):
        return self.endTime - self.startTime
