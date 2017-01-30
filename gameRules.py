"""
Michael Harrington

This file provides game rules and game abstractions
"""

from copy import copy, deepcopy
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
Rule helpers for rotating cardinal rays
"""

clockwise = { CardinalRay.down: CardinalRay.left,
              CardinalRay.left: CardinalRay.up,
              CardinalRay.up: CardinalRay.right,
              CardinalRay.right: CardinalRay.down
            }

counterClockwise = { CardinalRay.down: CardinalRay.right,
                     CardinalRay.left: CardinalRay.down,
                     CardinalRay.up: CardinalRay.left,
                     CardinalRay.right: CardinalRay.up
                   }

"""
Rule abstractions for actions
"""
class Moves():
    clockwise = 0
    counterClockwise = 1
    forward = 2
    backward = 3

class MovableObjs():
    boat = 0
    alligator = 1
    turtle = 2

class Action():
    def __init__(self, obj, act):
        self.obj = obj
        self.objIndex = 0
        self.act = act

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
    # Class Constants
    objLength = 3
    # Modified Variables
    numAlligators = 0

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

    @property
    def actions(self):
        return [ Action(MovableObjs.alligator, Moves.forward),
                 Action(MovableObjs.alligator, Moves.backward) ]

class Turtle(Animal):
    # Class Constants
    objLength = 2
    # Modified Variables
    numTurtles = 0

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

    @property
    def actions(self):
        return [ Action(MovableObjs.turtle, Moves.forward),
                 Action(MovableObjs.turtle, Moves.backward) ]

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

    @property
    def actions(self):
        return [ Action(MovableObjs.boat, Moves.forward),
                 Action(MovableObjs.boat, Moves.clockwise),
                 Action(MovableObjs.boat, Moves.counterClockwise) ]

    def move(self, action):
        if action.act == Moves.clockwise:
            self.posRay.cardDir = clockwise[self.posRay.cardDir]
        elif action.act == Moves.counterClockwise:
            self.posRay.cardDir = counterClockwise[self.posRay.cardDir]
        elif action.act == Moves.forward:
            pos = rayToVectorPointList(self.posRay, 2)[1]
            self.posRay.x = pos.x
            self.posRay.y = pos.y
        else:
            raise NotImplemented('Not a recognized boat action')
        

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
def createBoardState(board, radSrc, radMag, radDecF, boat, goal, alligs, turts, trees):
    return BoardState( board,
                       RadSource(radSrc, radMag, radDecF),
                       Boat(boat),
                       Goal(goal),
                       [Alligator(a) for a in alligs],
                       [Turtle(t) for t in turts],
                       [Tree(t) for t in trees] )

class BoardState():
    def __init__(self, board, radSrc, boat, goal, alligs, turtles, trees):
        self.board = board
        self.radSrc = radSrc
        self.boat = boat
        self.goal = goal
        self.alligators = alligs
        self.turtles = turtles
        self.trees = trees

    @property
    def actionObjects(self):
        return [self.boat] + self.alligators + self.turtles

    def applyAction(self, action):
        newBoat = deepcopy(self.boat)
        newAlligators = deepcopy(self.alligators)
        newTurtles = deepcopy(self.turtles)
        if action.obj == MovableObjs.boat:
            newBoat.move(action)
        elif action.obj == MovableObjs.alligator:
            pass
        elif action.obj == MovableObjs.turtle:
            pass
        else:
            raise NotImplementedError('Unimplemented movable action')

        return BoardState( self.board,
                           self.radSrc,
                           newBoat,
                           self.goal,
                           newAlligators,
                           newTurtles,
                           self.trees )

    def getNeighbors(self):
        for gameObj in self.actionObjects:
            for action in gameObj.actions:
                try:
                    newBoardState = self.applyAction(action)
                except ValueError:
                    continue
                yield newBoardState, action

    def __str__(self):
        stateStr = ''
        stateStr += _createStrLine(self.board.x, self.board.y)
        stateStr += _createStrLine(self.radSrc.location.x, self.radSrc.location.y)
        stateStr += _createStrLine(self.radSrc.magnitude, self.radSrc.decayFactor)
        stateStr += _createStrLine( len(self.alligators),
                                         len(self.turtles),
                                         len(self.trees) )
        for gameObj in (self.alligators + self.turtles + self.trees):
            stateStr += str(gameObj) + '\n'
        stateStr += str(self.boat) + '\n'
        stateStr += str(self.goal) + '\n'

        return stateStr

def isGoalState(boardState):
    return boardState.boat.collision(boardState.goal)

"""
Rule handling for state generation
"""
"""
Returns list of tuples of neighbor, action :: List(Tuple(BoardState, Action))
"""
def neighborGen(boardState):
    return boardState.getNeighbors()

