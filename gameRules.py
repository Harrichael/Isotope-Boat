"""
Michael Harrington

This file provides game rules and game abstractions
"""

from cartMath import CardinalRay

"""
Rule handling helpers for displaying text
"""
charDict = { CardinalRay.down: 'D',
             CardinalRay.up: 'U',
             CardinalRay.left: 'L',
             CardinalRay.right: 'R',
           }

def _createStr(*lineEls):
    return ' '.join(map(str, lineEls))

def _createStrLine(*lineEls):
    return _createStr(*lineEls) + '\n'

"""
Rule abstractions for game objects
"""
class RadSource():
    def __init__(self, srcPoint, magnitude, decayFactor):
        self.location = srcPoint
        self.magnitude = magnitude
        self.decayFactor = decayFactor

class MapEntity():
    pass

class Animal(MapEntity):
    def __init__(self, posRay):
        self.posRay = posRay

    @property
    def charDir(self):
        return charDict[self.posRay.cardDir]

    def __str__(self):
        return _createStr(self.posRay.x, self.posRay.y, self.charDir)

class Alligator(Animal):
    pass

class Turtle(Animal):
    pass

class Tree(MapEntity):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

class Boat(MapEntity):
    def __init__(self, posRay):
        self.posRay = posRay

    @property
    def charDir(self):
        return charDict[self.posRay.cardDir]

    def __str__(self):
        return _createStr(self.posRay.x, self.posRay.y, self.charDir)

"""
Rule handling for representing board state
"""
class BoardState():
    def __init__(self, board, radSrc, radMag, radDecayF, boat, goal, alligs, turtles, trees):
        self.board = board
        self.radSrc = RadSource(radSrc, radMag, radDecayF)
        self.boat = Boat(boat)
        self.goal = goal
        self.alligators = [Alligator(a) for a in alligs]
        self.turtles = [Turtle(t) for t in turtles]
        self.trees = [Tree(t) for t in trees]

    def __str__(self):
        stateStr = ''
        stateStr += _createStrLine(self.board.x, self.board.y)
        stateStr += _createStrLine(self.radSrc.location.x, self.radSrc.location.y)
        stateStr += _createStrLine(self.radSrc.magnitude, self.radSrc.decayFactor)
        stateStr += _createStrLine( len(self.alligators),
                                         len(self.turtles),
                                         len(self.trees) )
        for gameObj in list(self.alligators + self.turtles + self.trees):
            stateStr += str(gameObj) + '\n'
        stateStr += str(self.boat) + '\n'
        stateStr += _createStrLine( self.goal.x, self.goal.y )

        return stateStr

