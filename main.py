"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms and heuristics
in order to navigate a traffic jam like game with the
addition of a gradient cost field.
"""

from readPuzzleInput import getStateFromFile
from gameRules import neighborGen, isGoalState
from pathFinders import BFTS

"""
GameSolver class handles extracting file input, searching, and printing
"""
class GameSolver():
    def __init__(self):
        pass

    def runInputFile(self, inputFilePath):
        self.initialState = getStateFromFile(inputFilePath)
        solver = BFTS(self.initialState, neighborGen, (lambda s, d: 1), isGoalState)

    def printOutput(self):
        print self.initialState

if __name__ == '__main__':
    solver = GameSolver()
    solver.runInputFile('puzzles/examplePuzzle.txt')
    solver.printOutput()
