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
        self.boardDimensions = board
        self.radiationSource = radSrc
        self.radSource = RadSource(radSrc, radMag, radDecayF)
        self.goal = goal
