"""
Michael Harrington

This file provides heuristics for path finders
"""

from itertools import chain

from game.gameRules import MapEntity,Moves
from game.util.cartMath import manhattanDistance, rayToPointList

def getBoatNeighbors(boardState):
    for action in boardState.boat.actions:
        newBoardState = boardState.applyAction(action)
        if newBoardState:
            yield newBoardState, action

def canBoatAdvance(boardState):
    for action in boardState.boat.actions:
        if action.act == Moves.forward:
            return bool(boardState.applyAction(action))
    return False

def smartHeuristic(boardState):
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
    if not canBoatAdvance(boardState):
        boatMobility = 4 - len(list(getBoatNeighbors(boardState)))
    radGoalDistance = manhattanDistance(radPos, goalPos)
    goalDistance = manhattanDistance(boatPos, goalPos)
    goalWeight = (goalDistance + 5.0)/goalDistance
    radDistance = maxRadDist - manhattanDistance(boatPos, radPos)
    radWeight = (radGoalDistance + 1.0)/(radGoalDistance + 2.0) * (goalDistance - 1.0)/goalDistance
    return goalWeight*goalDistance + radWeight*radDistance + goalBlocked + boatMobility
