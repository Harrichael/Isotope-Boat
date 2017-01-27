"""
Michael Harrington

This file provides basic cartesian abstractions
"""

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CardinalRay():
    down = 0
    up = 1
    left = 2
    right = 3
    def __init__(self, x, y, cardDir):
        self.x = x
        self.y = y
        self.cardDir = cardDir
