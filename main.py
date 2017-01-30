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
        initialState = getStateFromFile(inputFilePath)
        pathSolver = BFTS(initialState, neighborGen, (lambda s, d: 1), isGoalState)
        if pathSolver.pathFound:
            self.path = pathSolver.actionPath
            self.finalState = pathSolver.boardStatePath[-1]
            return True
        return False

    def printOutput(self):
        print self.finalState

if __name__ == '__main__':
    gSolver = GameSolver()
    if gSolver.runInputFile('puzzles/puzzle1.txt'):
        gSolver.printOutput()
    else:
        print 'No solution found'
