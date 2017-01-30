"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms and heuristics
in order to navigate a traffic jam like game with the
addition of a gradient cost field.
"""

from timer import timeStampMS
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

        startTime = timeStampMS()
        self.pathSolver = BFTS(initialState, neighborGen, (lambda s, d: 1), isGoalState)
        endTime = timeStampMS()
        self.totalTime = endTime - startTime

        return self.pathSolver.pathFound

    def printOutput(self):
        path = self.pathSolver.actionPath
        finalSearchState = self.pathSolver.searchNodePath[-1]
        finalState = finalSearchState.boardState
        actions = self.pathSolver.actionPath

        print self.totalTime
        print finalSearchState.pathCost
        print len(actions)
        print ','.join(map(str, actions))
        print finalState

if __name__ == '__main__':
    gSolver = GameSolver()
    if gSolver.runInputFile('puzzles/puzzle1.txt'):
        gSolver.printOutput()
    else:
        print '(Error) No solution found'

