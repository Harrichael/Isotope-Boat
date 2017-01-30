"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms and heuristics
in order to navigate a traffic jam like game with the
addition of a gradient cost field.

TODO:
    Appropriate Turtle/Alligator Moves
    Save in solution1.txt
    Appropriate Exceptions
    Code Reduction
    Code Comments/Headers
    Profile
    Reduce Complexity
"""

from timer import timeStampMS
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

        startTime = timeStampMS()
        self.pathSolver = BFTS(initialState, neighborGen, costCalc, isGoalState)
        endTime = timeStampMS()
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

if __name__ == '__main__':
    gSolver = GameSolver()
    if gSolver.runInputFile('puzzles/puzzle1.txt'):
        output = gSolver.strOutput()
        with open('solutions/solution1.txt', 'w') as fileObj:
            fileObj.write(output)
    else:
        print '(Error) No solution found'

