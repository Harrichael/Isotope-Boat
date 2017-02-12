"""
Michael Harrington

Main Python File for Puzzle Project 1

This puzzle is using search algorithms (and a later phase, heuristics)
in order to navigate a traffic jam like game with the
addition of a gradient cost field dubbed a radiation field.

TODO:
objLength in gameRule files
CLI
heuristic in different file 
"""

from itertools import chain

from game.gameRules import MapEntity
from game.gameSolver import GameSolver
from game.util.pathFinders import BFTS, DLGS, IDDFGS, GrBFGS
from game.util.cartMath import manhattanDistance, rayToPointList

inputPuzzles = [ 'puzzle1.txt',
                 'puzzle2.txt',
               ]

outputFiles = [ 'solution1.txt',
                'solution2.txt',
              ]

def heuristic(boardState):
    if boardState.boat.collision(boardState.goal):
        return 0
    goalBlocked = 0
    obstacles = boardState.turtles + boardState.alligators
    if boardState.goal.collision(MapEntity(chain(*[obst.space for obst in obstacles]))):
        goalBlocked = 2
    return manhattanDistance(boardState.boat.cardRay.pos, boardState.goal.pos) + goalBlocked

if __name__ == '__main__':
    solver = GameSolver(lambda i, n, c, g: GrBFGS(i, n, c, g, heuristic))
    for inFile, outFile in zip(inputPuzzles, outputFiles):
        if solver.runInputFile('puzzles/' + inFile):
            output = solver.strOutput()
            with open('solutions/' + outFile, 'w') as fileObj:
                fileObj.write(output)
        else:
            print '(Error) No solution found'

