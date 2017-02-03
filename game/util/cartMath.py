"""
Michael Harrington

This file provides basic cartesian abstractions
"""

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, otherObj):
        return (self.x == otherObj.x) and (self.y == otherObj.y)

    def __hash__(self):
        return hash((self.x, self.y))

class Rectangle():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class CardinalRay():
    down = 0
    up = 1
    left = 2
    right = 3

    revDict = { down: up,
                up: down,
                right: left,
                left: right
              }

    def __init__(self, x, y, cardDir):
        self.x = x
        self.y = y
        self.cardDir = cardDir

    @property
    def pos(self):
        return Point(self.x, self.y)

    def reverse(self):
        self.cardDir = self.revDict[self.cardDir]

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.cardDir == other.cardDir)

    def __hash__(self):
        return hash((self.x, self.y, self.cardDir))

def manhattanDistance(src, dest):
    return abs(dest.x - src.x) + abs(dest.y - src.y)
