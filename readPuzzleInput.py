"""
Michael Harrington

This file provides functions to aid in reading puzzle input.
These functions return a board state given the input.
An error could be raised in the event of invalid input.
"""

from cartMath import Point, Rectangle, CardinalRay
from gameRules import createBoardState

"""
Input Format:
<boardWidth::Int> <boardHeigth::Int>
<radSourceX::Int> <radSourceY::Int>
<radMag::Int> <radDecayFactor::Int>
<numAlligs::Int> <numTurtles::Int> <numCypressTrees::Int>
for each allig:
    <algX::Int> <algY::Int> <algDir::Char>
for each turtle:
    <turtleX::Int> <turtleY::Int> <turtleDir::Char>
for each tree:
    <treeX::Int> <treeY::Int>
<boatX::Int> <boatY::Int> <boatDir::Char>
<goalX::Int> <goalY::Int>
"""

#TODO: sanitize inputs!
def getStateFromFile(inputFilePath):
    with open(inputFilePath) as fileObj:
        lines = fileObj.readlines()

    boardDimIn, radLocIn, radSpecIn, entityCountsIn, entityList, boatIn, goalIn = (
        lines[0], lines[1], lines[2], lines[3], lines[4:-2], lines[-2], lines[-1] )

    boardWidth, boardHeigth = _splitLineData(boardDimIn)
    radSourceX, radSourceY = _splitLineData(radLocIn)
    radMag, radDecayFactor = _splitLineData(radSpecIn)
    numAlligators, numTurtles, numTrees = _splitLineData(entityCountsIn, 3)
    boatX, boatY, boatDir = _splitLineData(boatIn)
    goalX, goalY = _splitLineData(goalIn)

    alligatorsIn, turtlesIn, treesIn = ( entityList[:numAlligators],
                                         entityList[numAlligators:numAlligators+numTurtles],
                                         entityList[numAlligators+numTurtles:] )

    alligators = []
    for alligIn in alligatorsIn:
        alligators.append( _createCardRay( *_splitLineData(alligIn) ) )

    turtles = []
    for turtIn in turtlesIn:
        turtles.append( _createCardRay( *_splitLineData(turtIn) ) )

    trees = []
    for treeIn in treesIn:
        trees.append( Point( *_splitLineData(treeIn) ) )
        
    return createBoardState( Rectangle(boardWidth, boardHeigth),
                             Point(radSourceX, radSourceY),
                             radMag,
                             radDecayFactor,
                             _createCardRay(boatX, boatY, boatDir),
                             Point(goalX, goalY),
                             alligators,
                             turtles,
                             trees
                           )

def _splitLineData(line, numInts=2):
    items = line.split()
    for i in range(numInts):
        items[i] = int(items[i])
    return items

def _createCardRay(x, y, dirChar):
    if dirChar == 'D':
        cardDir = CardinalRay.down
    elif dirChar == 'U':
        cardDir = CardinalRay.up
    elif dirChar == 'L':
        cardDir = CardinalRay.left
    elif dirChar == 'R':
        cardDir = CardinalRay.right
    else:
        raise ValueError('Direction not supported: ' + dirChar)

    return CardinalRay(x, y, cardDir)
