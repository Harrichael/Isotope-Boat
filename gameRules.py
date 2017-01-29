"""
Michael Harrington

This file provides game rules and game abstractions
"""

from cartMath import Point, CardinalRay

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
    def collision(self, otherObj):
        for point in self.space:
            if point in otherObj.space:
                return True
        return False

    @property
    def space(self):
        raise NotImplemented('MapEntity derived classes must implement space')

def rayToVectorPointList(posRay, vectorLength):
    if posRay.cardDir == posRay.down:
        nextP = lambda p: Point(p.x, p.y+1)
    elif posRay.cardDir == posRay.up:
        nextP = lambda p: Point(p.x, p.y-1)
    elif posRay.cardDir == posRay.left:
        nextP = lambda p: Point(p.x-1, p.y)
    elif posRay.cardDir == posRay.right:
        nextP = lambda p: Point(p.x+1, p.y)
    else:
        raise ValueError('Invalid Cartesian Direction')

    pointList = [posRay.pos]
    for index in range(vectorLength-1):
        pointList.append(nextP(pointList[index]))
    return pointList

class Animal(MapEntity):
    def __init__(self, posRay):
        self.posRay = posRay

    @property
    def charDir(self):
        return charDict[self.posRay.cardDir]

    def __str__(self):
        return _createStr(self.posRay.x, self.posRay.y, self.charDir)

class Alligator(Animal):
    objLength = 3

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

class Turtle(Animal):
    objLength = 2

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

class Tree(MapEntity):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

    @property
    def space(self):
        return set([self.pos])

class Boat(MapEntity):
    objLength = 2
    def __init__(self, posRay):
        self.posRay = posRay

    @property
    def charDir(self):
        return charDict[self.posRay.cardDir]

    def __str__(self):
        return _createStr(self.posRay.x, self.posRay.y, self.charDir)

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

class Goal(MapEntity):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

    @property
    def space(self):
        return set([self.pos])

"""
Rule handling for representing board state
"""
class BoardState():
    def __init__(self, board, radSrc, radMag, radDecayF, boat, goal, alligs, turtles, trees):
        self.board = board
        self.radSrc = RadSource(radSrc, radMag, radDecayF)
        self.boat = Boat(boat)
        self.goal = Goal(goal)
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
        stateStr += str(self.goal) + '\n'

        return stateStr

def isGoalState(boardState):
    return boardState.boat.collision(boardState.goal)

"""
Rule handling for state generation
"""
def neighborGen(boardState):
    return []

