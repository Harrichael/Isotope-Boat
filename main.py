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
                 'puzzle3.txt',
               ]

outputFiles = [ 'solution1.txt',
                'solution2.txt',
                'solution3.txt',
              ]

def heuristic(boardState):
    if boardState.boat.collision(boardState.goal):
        return 0
    boatPos = boardState.boat.cardRay.pos
    goalPos = boardState.goal.pos
    radPos = boardState.radSrc.pos
    turtles = boardState.turtles
    alligators = boardState.alligators
    boardPos = boardState.board.pos
    maxRadDist = max(boardPos.x - radPos.x, radPos.x) + max(boardPos.y - radPos.y, radPos.y)

    goalBlocked = 0
    if boardState.goal.collision(MapEntity(chain(*[t.space for t in turtles]))):
        goalBlocked = 2
    elif boardState.goal.collision(MapEntity(chain(*[a.space for a in alligators]))):
        goalBlocked = 3
    boatMobility = 0
    if not boardState.canBoatAdvance():
        boatMobility = 4 - len(list(boardState.getBoatNeighbors()))
    radGoalDistance = manhattanDistance(radPos, goalPos)
    goalDistance = manhattanDistance(boatPos, goalPos)
    goalWeight = (goalDistance + 5.0)/goalDistance
    radDistance = maxRadDist - manhattanDistance(boatPos, radPos)
    radWeight = radGoalDistance/(radGoalDistance + 1.0) * (goalDistance - 1.0)/goalDistance
    return goalWeight*goalDistance + radWeight*radDistance + goalBlocked + boatMobility

if __name__ == '__main__':
    solver = GameSolver(lambda i, n, c, g: GrBFGS(i, n, c, g, heuristic))
    for inFile, outFile in zip(inputPuzzles, outputFiles):
        if solver.runInputFile('puzzles/' + inFile):
            output = solver.strOutput()
            with open('solutions/' + outFile, 'w') as fileObj:
                fileObj.write(output)
        else:
            print '(Error) No solution found'

