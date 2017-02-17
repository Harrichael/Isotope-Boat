"""
Michael Harrington

This file exposes the game solver class that solves the puzzle
"""

from util.timer import timeStampMuS
from readPuzzleInput import getStateFromFile
from gameRules import neighborGen, isGoalState, costCalc

"""
GameSolver class handles extracting file input, searching, and printing
"""
class GameSolver():
    def __init__(self, solverAlg):
        self.solverAlg = solverAlg

    def runInputFile(self, inputFilePath):
        initialState = getStateFromFile(inputFilePath)

        startTime = timeStampMuS()
        self.pathSolver = self.solverAlg(initialState, neighborGen, costCalc, isGoalState)
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
