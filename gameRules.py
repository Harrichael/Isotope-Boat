"""
Michael Harrington

This file provides game rules and game abstractions
"""

from copy import copy, deepcopy
from cartMath import Point, CardinalRay, ManhattanDistance

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

    moveDict = { clockwise: 'C',
                 counterClockwise: 'N',
                 forward: 'F',
                 backward: 'B'
               }

class MovableObjs():
    boat = 0
    alligator = 1
    turtle = 2

    objDict = { boat: 'B',
                alligator: 'A',
                turtle: 'T',
              }

class Action():
    def __init__(self, obj, act, cardDir=None):
        self.obj = obj
        self.objIndex = 0
        self.act = act
        # Some Actions might want to override our beloved forward/backward printing
        self.cardDir = cardDir

    def __str__(self):
        dirChar = Moves.moveDict[self.act] if self.cardDir == None else charDict[self.cardDir]
        return ' '.join([ MovableObjs.objDict[self.obj],
                          str(self.objIndex),
                          dirChar
                       ])

"""
Rule abstractions for game objects
"""
class RadSource():
    def __init__(self, srcPoint, magnitude, decayFactor):
        self.location = srcPoint
        self.magnitude = magnitude
        self.decayFactor = decayFactor

    def rads(self, point):
        distance = ManhattanDistance(self.location, point)
        return self.magnitude - self.decayFactor * distance

class MapEntity():
    def __init__(self, pointList):
        self._space = pointList

    def collision(self, otherObj):
        for point in self.space:
            if point in otherObj.space:
                return True
        return False

    @property
    def space(self):
        return self._space

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

    def contained(self, points):
        return all([point in self.space for point in points])

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

class Animal(MapEntity):
    @property
    def charDir(self):
        return charDict[self.posRay.cardDir]

    def __str__(self):
        return _createStr(self.posRay.x, self.posRay.y, self.charDir)

    def move(self, action):
        if action.act == Moves.forward:
            pos = rayToVectorPointList(self.posRay, 2)[1]
            self.posRay.x = pos.x
            self.posRay.y = pos.y
        elif action.act == Moves.backward:
            self.posRay.reverse()
            pos = rayToVectorPointList(self.posRay, 2)[1]
            self.posRay.reverse()
            self.posRay.x = pos.x
            self.posRay.y = pos.y
        else:
            raise NotImplemented('Not a recognized boat action')
        return MapEntity([])

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
        return [ Action(MovableObjs.alligator, Moves.forward, self.posRay.cardDir),
                 Action(MovableObjs.alligator, Moves.backward, self.posRay.cardDir) ]

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
        return [ Action(MovableObjs.turtle, Moves.forward, self.posRay.cardDir),
                 Action(MovableObjs.turtle, Moves.backward, self.posRay.cardDir) ]

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
        return [ Action(MovableObjs.boat, Moves.forward, self.posRay.cardDir),
                 Action(MovableObjs.boat, Moves.clockwise),
                 Action(MovableObjs.boat, Moves.counterClockwise) ]

    def move(self, action):
        movePoints = []
        frontPos = rayToVectorPointList(self.posRay, 2)[1]
        if action.act == Moves.clockwise:
            self.posRay.cardDir = clockwise[self.posRay.cardDir]
            newFrontPos = rayToVectorPointList(self.posRay, 2)[1]
            movePoints.append(Point(newFrontPos.x, frontPos.y))
            movePoints.append(Point(frontPos.x, newFrontPos.y))
        elif action.act == Moves.counterClockwise:
            self.posRay.cardDir = counterClockwise[self.posRay.cardDir]
            newFrontPos = rayToVectorPointList(self.posRay, 2)[1]
            movePoints.append(Point(newFrontPos.x, frontPos.y))
            movePoints.append(Point(frontPos.x, newFrontPos.y))
        elif action.act == Moves.forward:
            self.posRay.x = frontPos.x
            self.posRay.y = frontPos.y
        else:
            raise NotImplemented('Not a recognized boat action')
        return MapEntity(movePoints)
        

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
        newBoat = deepcopy(self.boat)
        newAlligators = deepcopy(self.alligators)
        newTurtles = deepcopy(self.turtles)
        index = action.objIndex
        if action.obj == MovableObjs.boat:
            actionObj = newBoat
            obstacles = (newAlligators + newTurtles + self.trees)

        elif action.obj == MovableObjs.alligator:
            actionObj = newAlligators[index]
            otherAlligators = newAlligators[:index] + newAlligators[index+1:]
            obstacles = ([newBoat] + otherAlligators + newTurtles + self.trees)

        elif action.obj == MovableObjs.turtle:
            actionObj = newTurtles[index]
            otherTurtles = newTurtles[:index] + newTurtles[index+1:]
            obstacles = ([newBoat] + newAlligators + otherTurtles + self.trees)

        else:
            raise NotImplementedError('Unimplemented movable action')
        movePoints = actionObj.move(action)
        if not self.board.contained:
            raise ValueError

        for obj in obstacles:
            if obj.collision(actionObj) or obj.collision(movePoints):
                raise ValueError

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
"""
Returns list of tuples of neighbor, action :: List(Tuple(BoardState, Action))
"""
def neighborGen(boardState):
    return boardState.getNeighbors()

"""
Rule handling for cost calculation
"""
def costCalc(boardState):
    return sum([boardState.radSrc.rads(point) for point in boardState.boat.space])

