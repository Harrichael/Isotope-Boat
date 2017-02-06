"""
Michael Harrington

This file provides game rules and game abstractions
"""

from itertools import chain
from copy import copy
from random import shuffle

from util.cartMath import ( Point,
                            Cardinal,
                            CardinalRay,
                            manhattanDistance,
                            rayToPointList,
                          )

"""
Action Rules

Boat, alligator, and turtle are movable game objects.
Each turn, one thing can be moved, represented by Action().
Possible moves are clockwise, counterClockwise, forward, and
backward. Each movable object will return their valid actions
created using the Action class.
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

    def __eq__(self, other):
        return all([ self.obj == other.obj,
                     self.objIndex == other.objIndex,
                     self.act == other.act
                  ])

    def __ne__(self, other):
        return not self == other

"""
Text Display Rules

This section defines some text displaying helpers.
In addition to translating directions, move types,
and object types, this section provides helper methods
space joining.
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
Game Object Rules

Game objects, like goals, boat, and other movable objects
are represented here. A MapEntity has some spacial interactions.
Radiation sources do not collide with any object.

Actions property returns list of potential actions the object can
take. Move function applies an action and returns a mapentity
object that must be empty for the move to be successful.
"""
class RadSource():
    def __init__(self, srcPoint, magnitude, decayFactor):
        self.location = srcPoint
        self.magnitude = magnitude
        self.decayFactor = decayFactor

    def rads(self, point):
        distance = manhattanDistance(self.location, point)
        return self.magnitude - self.decayFactor * distance

    def __eq__(self, other):
        return all([ self.location == other.location,
                     self.magnitude == other.magnitude,
                     self.decayFactor == other.decayFactor
                  ])

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.location, self.magnitude, self.decayFactor))

class MapEntity():
    def __init__(self, pointList):
        self._space = set(pointList)

    def collision(self, otherObj):
        return set.intersection(self.space, otherObj.space)

    @property
    def space(self):
        return self._space

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

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.pos)

class Animal(MapEntity):
    @property
    def charDir(self):
        return DisplayChar.ray[self.cardRay.cardDir]

    def __str__(self):
        return _createStr(self.cardRay.x, self.cardRay.y, self.charDir)

    def move(self, action):
        # Apply action but return a MapEntity that must be checked to validate move
        if action.act == Moves.forward:
            pos = rayToPointList(self.cardRay, 2)[1]
            self.cardRay.x = pos.x
            self.cardRay.y = pos.y
        elif action.act == Moves.backward:
            self.cardRay.reverseRay()
            pos = rayToPointList(self.cardRay, 2)[1]
            self.cardRay.reverseRay()
            self.cardRay.x = pos.x
            self.cardRay.y = pos.y
        else:
            raise NotImplementedError('Not a recognized boat action')
        return MapEntity(self.space)

class Alligator(Animal):
    objLength = 3

    def __init__(self, cardRay, index):
        self.cardRay = cardRay
        self.index = index

    @property
    def space(self):
        return set(rayToPointList(self.cardRay, self.objLength))

    @property
    def actions(self):
        obj = MovableObjs.alligator
        idx = self.index
        cardDir = self.cardRay.cardDir
        return [ Action(obj, Moves.forward, idx, cardDir),
                 Action(obj, Moves.backward, idx, Cardinal.reverse[cardDir]) ]

    def __copy__(self):
        a = Alligator(CardinalRay(self.cardRay.x, self.cardRay.y, self.cardRay.cardDir), self.index)
        return a

    def __eq__(self, other):
        return self.cardRay == other.cardRay and self.index == other.index

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.cardRay, self.index))

class Turtle(Animal):
    objLength = 2

    def __init__(self, cardRay, index):
        self.cardRay = cardRay
        self.index = index

    @property
    def space(self):
        return set(rayToPointList(self.cardRay, self.objLength))

    @property
    def actions(self):
        obj = MovableObjs.turtle
        idx = self.index
        cardDir = self.cardRay.cardDir
        return [ Action(obj, Moves.forward, idx, cardDir),
                 Action(obj, Moves.backward, idx, Cardinal.reverse[cardDir]) ]

    def __copy__(self):
        t = Turtle(CardinalRay(self.cardRay.x, self.cardRay.y, self.cardRay.cardDir), self.index)
        return t

    def __eq__(self, other):
        return self.cardRay == other.cardRay and self.index == other.index

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.cardRay, self.index))

class Tree(MapEntity):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

    @property
    def space(self):
        return set([self.pos])

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.pos)

class Boat(MapEntity):
    objLength = 2

    def __init__(self, cardRay, index):
        self.cardRay = cardRay
        self.index = index

    @property
    def charDir(self):
        return DisplayChar.ray[self.cardRay.cardDir]

    def __str__(self):
        return _createStr(self.cardRay.x, self.cardRay.y, self.charDir)

    @property
    def space(self):
        return set(rayToPointList(self.cardRay, self.objLength))

    @property
    def actions(self):
        return [ Action(MovableObjs.boat, Moves.forward, self.index, self.cardRay.cardDir),
                 Action(MovableObjs.boat, Moves.counterClockwise, self.index),
                 Action(MovableObjs.boat, Moves.clockwise, self.index) ]

    def move(self, action):
        # Apply action but return a MapEntity that must be checked to validate move
        movePoints = set()
        frontPos = rayToPointList(self.cardRay, 2)[1]
        if action.act == Moves.clockwise:
            self.cardRay.cardDir = Cardinal.clockwise[self.cardRay.cardDir]
            newFrontPos = rayToPointList(self.cardRay, 2)[1]
            movePoints.add(Point(newFrontPos.x, frontPos.y))
            movePoints.add(Point(frontPos.x, newFrontPos.y))
        elif action.act == Moves.counterClockwise:
            self.cardRay.cardDir = Cardinal.counterClockwise[self.cardRay.cardDir]
            newFrontPos = rayToPointList(self.cardRay, 2)[1]
            movePoints.add(Point(newFrontPos.x, frontPos.y))
            movePoints.add(Point(frontPos.x, newFrontPos.y))
        elif action.act == Moves.forward:
            self.cardRay.x = frontPos.x
            self.cardRay.y = frontPos.y
        else:
            raise NotImplementedError('Not a recognized boat action')
        return MapEntity(movePoints.union(self.space))

    def __copy__(self):
        b = Boat(CardinalRay(self.cardRay.x, self.cardRay.y, self.cardRay.cardDir), self.index)
        return b

    def __eq__(self, other):
        return self.cardRay == other.cardRay and self.index == other.index

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.cardRay, self.index))

class Goal(MapEntity):
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return _createStr(self.pos.x, self.pos.y)

    @property
    def space(self):
        return set([self.pos])

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.pos)

"""
Board State Rules

BoardState holds the game objects for a defined state.
The function applyAction can return a successor boardstate
given a valid action.
"""
def createBoardState(board, radSrc, radMag, radDecF, boat, goal, alligs, turts, trees):
    # radSrc :: CardinalRay
    # radMag, radDecF :: Int
    # boat :: CardinalRay
    # goal :: Point
    # alligs, turts, trees :: [CardinalRay]
    return BoardState( Board(board),
                       RadSource(radSrc, radMag, radDecF),
                       Boat(boat, index=0),
                       Goal(goal),
                       [Alligator(a, index) for index, a in enumerate(alligs)],
                       [Turtle(t, index) for index, t in enumerate(turts)],
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
        # Lets return a successor board state but return None if action is invalid.
        # Also, you need copies of some objects.
        index = action.objIndex
        if action.obj == MovableObjs.boat:
            newBoat = copy(self.boat)
            newAlligators = self.alligators
            newTurtles = self.turtles
            actionObj = newBoat
            obstacles = (newAlligators + newTurtles + self.trees)

        elif action.obj == MovableObjs.alligator:
            newBoat = self.boat
            newAlligators = copy(self.alligators)
            newTurtles = self.turtles
            actionObj = copy(newAlligators[index])
            newAlligators[index] = actionObj
            otherAlligators = newAlligators[:index] + newAlligators[index+1:]
            obstacles = ([newBoat] + otherAlligators + newTurtles + self.trees)

        elif action.obj == MovableObjs.turtle:
            newBoat = self.boat
            newAlligators = self.alligators
            newTurtles = copy(self.turtles)
            actionObj = copy(newTurtles[index])
            newTurtles[index] = actionObj
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
            actions = gameObj.actions
            shuffle(actions)
            for action in actions:
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

    def __eq__(self, other):
        if self.boat != other.boat:
            return False
        for selfTurtle, otherTurtle in zip(self.turtles, other.turtles):
            if selfTurtle != otherTurtle:
                return False
        for selfAlligator, otherAlligator in zip(self.alligators, other.alligators):
            if selfAlligator != otherAlligator:
                return False
        for selfTree, otherTree in zip(self.trees, other.trees):
            if selfTree != otherTree:
                return False
        if any([ len(other.trees) != len(self.trees),
                 len(other.alligators) != len(self.alligators),
                 len(other.turtles) != len(self.turtles),
                 self.goal != other.goal,
                 self.radSrc != other.radSrc,
                 self.goal != other.goal,
              ]):
            return False

        return True

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(( self.board,
                      self.radSrc,
                      self.boat,
                      self.goal,
                      tuple(self.alligators),
                      tuple(self.turtles),
                      tuple(self.trees)
                   ))

def isGoalState(boardState):
    return boardState.boat.collision(boardState.goal)

"""
This section provides helper functions to pass to search
algorithms.
"""
def neighborGen(boardState):
    return boardState.getNeighbors()

def costCalc(boardState):
    return sum([boardState.radSrc.rads(point) for point in boardState.boat.space])

