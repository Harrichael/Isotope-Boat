"""
Michael Harrington

This file provides game rules and game abstractions
"""

from itertools import chain
from copy import copy, deepcopy

from util.cartMath import Point, Cardinal, CardinalRay, manhattanDistance

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
    def __init__(self, obj, act, index, cardDir=None):
        self.obj = obj
        self.objIndex = index
        self.act = act
        # Some Actions might want to override our beloved forward/backward printing
        self.cardDir = cardDir

    def __str__(self):
        if self.cardDir == None:
            dirChar = DisplayChar.move[self.act]
        else:
            dirChar = DisplayChar.ray[self.cardDir]

        return ' '.join([ DisplayChar.obj[self.obj],
                          str(self.objIndex),
                          dirChar
                       ])

"""
Text Display Helpers
"""
class DisplayChar():
    ray = { Cardinal.down:  'D',
            Cardinal.up:    'U',
            Cardinal.left:  'L',
            Cardinal.right: 'R',
          }

    move = { Moves.clockwise:        'C',
             Moves.counterClockwise: 'N',
             Moves.forward:          'F',
             Moves.backward:         'B'
           }

    obj = { MovableObjs.boat:      'B',
            MovableObjs.alligator: 'A',
            MovableObjs.turtle:    'T',
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

    def rads(self, point):
        distance = manhattanDistance(self.location, point)
        return self.magnitude - self.decayFactor * distance

class MapEntity():
    def __init__(self, pointList):
        self._space = set(pointList)

    def collision(self, otherObj):
        return set.intersection(self.space, otherObj.space)

    @property
    def space(self):
        return self._space

nextPDict = { Cardinal.down: lambda p: Point(p.x, p.y+1),
              Cardinal.up: lambda p: Point(p.x, p.y-1),
              Cardinal.left: lambda p: Point(p.x-1, p.y),
              Cardinal.right: lambda p: Point(p.x+1, p.y)
            }

def rayToVectorPointList(posRay, vectorLength):
    nextP = nextPDict[posRay.cardDir]

    # We get a minor speed up by preallocating the list
    pointList = [posRay.pos]*vectorLength
    for index in range(vectorLength-1):
        pointList[index+1] = nextP(pointList[index])
    return pointList

class Board(MapEntity):
    def __init__(self, pos):
        self.pos = pos
        self._space = None

    @property
    def space(self):
        if not self._space:
            self._space = set()
            for x in range(self.pos.x):
                for y in range(self.pos.y):
                    self._space.add(Point(x, y))
        return self._space

    def contains(self, points):
        return points.issubset(self.space)

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

class Animal(MapEntity):
    @property
    def charDir(self):
        return DisplayChar.ray[self.posRay.cardDir]

    def __str__(self):
        return _createStr(self.posRay.x, self.posRay.y, self.charDir)

    def move(self, action):
        if action.act == Moves.forward:
            pos = rayToVectorPointList(self.posRay, 2)[1]
            self.posRay.x = pos.x
            self.posRay.y = pos.y
        elif action.act == Moves.backward:
            self.posRay.reverseRay()
            pos = rayToVectorPointList(self.posRay, 2)[1]
            self.posRay.reverseRay()
            self.posRay.x = pos.x
            self.posRay.y = pos.y
        else:
            raise NotImplementedError('Not a recognized boat action')
        return MapEntity(self.space)

class Alligator(Animal):
    # Class Constants
    objLength = 3
    # Modified Variables
    numAlligators = 0

    def __init__(self, posRay):
        self.posRay = posRay
        self.index = self.numAlligators
        self.__class__.numAlligators += 1

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

    @property
    def actions(self):
        obj = MovableObjs.alligator
        idx = self.index
        cardDir = self.posRay.cardDir
        return [ Action(obj, Moves.forward, idx, cardDir),
                 Action(obj, Moves.backward, idx, Cardinal.reverse[cardDir]) ]

    def __copy__(self):
        self.__class__.numAlligators -= 1
        a = Alligator(CardinalRay(self.posRay.x, self.posRay.y, self.posRay.cardDir))
        a.index = self.index
        return a

class Turtle(Animal):
    # Class Constants
    objLength = 2
    # Modified Variables
    numTurtles = 0

    def __init__(self, posRay):
        self.posRay = posRay
        self.index = self.numTurtles
        self.__class__.numTurtles += 1

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

    @property
    def actions(self):
        obj = MovableObjs.turtle
        idx = self.index
        cardDir = self.posRay.cardDir
        return [ Action(obj, Moves.forward, idx, cardDir),
                 Action(obj, Moves.backward, idx, Cardinal.reverse[cardDir]) ]

    def __copy__(self):
        self.__class__.numTurtles -= 1
        t = Turtle(CardinalRay(self.posRay.x, self.posRay.y, self.posRay.cardDir))
        t.index = self.index
        return t

class Tree(MapEntity):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

    @property
    def space(self):
        return set([self.pos])

class Boat(MapEntity):
    # Class Constants
    objLength = 2
    # Modified Variables
    numBoats = 0

    def __init__(self, posRay):
        self.posRay = posRay
        self.index = self.numBoats
        self.__class__.numBoats += 1

    @property
    def charDir(self):
        return DisplayChar.ray[self.posRay.cardDir]

    def __str__(self):
        return _createStr(self.posRay.x, self.posRay.y, self.charDir)

    @property
    def space(self):
        return set(rayToVectorPointList(self.posRay, self.objLength))

    @property
    def actions(self):
        return [ Action(MovableObjs.boat, Moves.forward, self.index, self.posRay.cardDir),
                 Action(MovableObjs.boat, Moves.counterClockwise, self.index),
                 Action(MovableObjs.boat, Moves.clockwise, self.index) ]

    def move(self, action):
        movePoints = set()
        frontPos = rayToVectorPointList(self.posRay, 2)[1]
        if action.act == Moves.clockwise:
            self.posRay.cardDir = Cardinal.clockwise[self.posRay.cardDir]
            newFrontPos = rayToVectorPointList(self.posRay, 2)[1]
            movePoints.add(Point(newFrontPos.x, frontPos.y))
            movePoints.add(Point(frontPos.x, newFrontPos.y))
        elif action.act == Moves.counterClockwise:
            self.posRay.cardDir = Cardinal.counterClockwise[self.posRay.cardDir]
            newFrontPos = rayToVectorPointList(self.posRay, 2)[1]
            movePoints.add(Point(newFrontPos.x, frontPos.y))
            movePoints.add(Point(frontPos.x, newFrontPos.y))
        elif action.act == Moves.forward:
            self.posRay.x = frontPos.x
            self.posRay.y = frontPos.y
        else:
            raise NotImplementedError('Not a recognized boat action')
        return MapEntity(movePoints.union(self.space))

    def __copy__(self):
        self.__class__.numBoats -= 1
        b = Boat(CardinalRay(self.posRay.x, self.posRay.y, self.posRay.cardDir))
        b.index = self.index
        return b
        

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
    return BoardState( Board(board),
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
        index = action.objIndex
        if action.obj == MovableObjs.boat:
            newBoat = copy(self.boat)
            newAlligators = self.alligators
            newTurtles = self.turtles
            actionObj = newBoat
            obstacles = (newAlligators + newTurtles + self.trees)

        elif action.obj == MovableObjs.alligator:
            newBoat = self.boat
            newAlligators = deepcopy(self.alligators)
            newTurtles = self.turtles
            actionObj = newAlligators[index]
            otherAlligators = newAlligators[:index] + newAlligators[index+1:]
            obstacles = ([newBoat] + otherAlligators + newTurtles + self.trees)

        elif action.obj == MovableObjs.turtle:
            newBoat = self.boat
            newAlligators = self.alligators
            newTurtles = deepcopy(self.turtles)
            actionObj = newTurtles[index]
            otherTurtles = newTurtles[:index] + newTurtles[index+1:]
            obstacles = ([newBoat] + newAlligators + otherTurtles + self.trees)

        else:
            raise NotImplementedError('Unimplemented movable action')

        moveEntity = actionObj.move(action)
        if not self.board.contains(moveEntity.space):
            return None

        obstacleEntity = MapEntity(chain(*[obst.space for obst in obstacles]))
        if moveEntity.collision(obstacleEntity):
            return None

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
                newBoardState = self.applyAction(action)
                if newBoardState:
                    yield newBoardState, action

    def __str__(self):
        stateStr = ''
        stateStr += str(self.board) + '\n'
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
def neighborGen(boardState):
    return boardState.getNeighbors()

"""
Rule handling for cost calculation
"""
def costCalc(boardState):
    return sum([boardState.radSrc.rads(point) for point in boardState.boat.space])

