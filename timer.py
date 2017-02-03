"""
Michael Harrington

This file provides function for timeing and profiling
"""

from cProfile import Profile
from time import time

def timeStampMuS():
    return int(round(time() * 1000000))

def profile(func):
    def wrapper(*args, **kwargs):
        prof = Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.print_stats(sort='time')
        return retval

    return wrapper
