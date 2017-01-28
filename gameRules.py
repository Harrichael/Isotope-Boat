"""
Michael Harrington

This file provides game rules and game abstractions
"""

class RadSource():
    def __init__(self, srcPoint, magnitude, decayFactor):
        self.location = srcPoint
        self.magnitude = magnitude
        self.decayFactor = decayFactor

class BoardState():
    def __init__(self, board, radSrc, radMag, radDecayF, boat, goal, alligs, turtles, trees):
        self.board = board
        self.radSrc = RadSource(radSrc, radMag, radDecayF)
        self.boat = boat
        self.goal = goal
        self.alligators = alligs
        self.turtles = turtles
        self.trees = trees
        

    def __str__(self):
        stateStr = ''
        stateStr += self._createStrLine(self.board.x, self.board.y)
        stateStr += self._createStrLine(self.radSrc.location.x, self.radSrc.location.y)
        stateStr += self._createStrLine(self.radSrc.magnitude, self.radSrc.decayFactor)
        stateStr += self._createStrLine( len(self.alligators),
                                         len(self.turtles),
                                         len(self.trees) )
        stateStr += self._createStrLine( self.boat.x, self.boat.y )
        stateStr += self._createStrLine( self.goal.x, self.goal.y )

        return stateStr

    @staticmethod
    def _createStrLine(*lineEls):
        return ' '.join(map(str, lineEls)) + '\n'

