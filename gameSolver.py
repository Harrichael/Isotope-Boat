"""
Michael Harrington

This file exposes the game solver class that solves the puzzle
"""

from timer import timeStampMuS
from readPuzzleInput import getStateFromFile
from gameRules import neighborGen, isGoalState, costCalc
from pathFinders import BFTS

"""
GameSolver class handles extracting file input, searching, and printing
"""
class GameSolver():
    def __init__(self):
        pass

    def runInputFile(self, inputFilePath):
        initialState = getStateFromFile(inputFilePath)

        startTime = timeStampMuS()
        self.pathSolver = BFTS(initialState, neighborGen, costCalc, isGoalState)
        endTime = timeStampMuS()
        self.totalTime = endTime - startTime

        return self.pathSolver.pathFound

    def strOutput(self):
        path = self.pathSolver.actionPath
        finalSearchState = self.pathSolver.searchNodePath[-1]
        finalState = finalSearchState.boardState
        actions = self.pathSolver.actionPath
        pathCost = 0 if finalSearchState is None else finalSearchState.parent.pathCost

        return '\n'.join(map(str, [ self.totalTime,
                                    pathCost,
                                    len(actions),
                                    ','.join(map(str, actions)),
                                    finalState
                                  ]))
