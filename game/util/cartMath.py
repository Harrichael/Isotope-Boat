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

class Cardinal():
    down = 0
    up = 1
    left = 2
    right = 3

    reverse = { down:  up,
                up:    down,
                right: left,
                left:  right
              }

    clockwise = { down:  left,
                  left:  up,
                  up:    right,
                  right: down
                }

    counterClockwise = { down:  right,
                         left:  down,
                         up:    left,
                         right: up
                       }

class CardinalRay(Cardinal):
    def __init__(self, x, y, cardDir):
        self.x = x
        self.y = y
        self.cardDir = cardDir

    @property
    def pos(self):
        return Point(self.x, self.y)

    def reverseRay(self):
        self.cardDir = self.reverse[self.cardDir]

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.cardDir == other.cardDir)

    def __hash__(self):
        return hash((self.x, self.y, self.cardDir))

def manhattanDistance(src, dest):
    return abs(dest.x - src.x) + abs(dest.y - src.y)

nextPDict = { Cardinal.down: lambda p: Point(p.x, p.y+1),
              Cardinal.up: lambda p: Point(p.x, p.y-1),
              Cardinal.left: lambda p: Point(p.x-1, p.y),
              Cardinal.right: lambda p: Point(p.x+1, p.y)
            }

def rayToPointList(posRay, vectorLength):
    nextP = nextPDict[posRay.cardDir]

    # We get a minor speed up by preallocating the list
    pointList = [posRay.pos]*vectorLength
    for index in range(vectorLength-1):
        pointList[index+1] = nextP(pointList[index])
    return pointList
