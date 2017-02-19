"""
Michael Harrington

This file provides some generic helpers that you
might want to use when creating a command line
interpreter. These may not directly relate to
the cmd module.
"""

import sys

def isInputPiped():
    return not sys.stdin.isatty()
