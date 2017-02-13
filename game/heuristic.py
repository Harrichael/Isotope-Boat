"""
Michael Harrington

This file provides heuristics for path finders
"""

from itertools import chain

from game.gameRules import MapEntity, Moves
from game.util.cartMath import manhattanDistance, rayToPointList, Point

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
    # If goal is made, give it best priority!
    if boardState.boat.collision(boardState.goal):
        return 0

    # Lets make some helper values
    boatPos = boardState.boat.cardRay.pos
    goalPos = boardState.goal.pos
    radPos = boardState.radSrc.pos
    turtles = boardState.turtles
    alligators = boardState.alligators
    boardPos = boardState.board.pos
    maxRadDist = max(boardPos.x - radPos.x, radPos.x) + max(boardPos.y - radPos.y, radPos.y)

    # If the goal is blocked we can't win
    goalBlocked = 0
    if boardState.goal.collision(MapEntity(chain(*[t.space for t in turtles]))):
        goalBlocked = 2
    elif boardState.goal.collision(MapEntity(chain(*[a.space for a in alligators]))):
        goalBlocked = 3
    # If we can't advance forward, can we at least turn?
    boatMobility = 0
    if not canBoatAdvance(boardState):
        boatMobility = 4 - len(list(getBoatNeighbors(boardState)))
    # This value is used later for weighting, if the rad src is close to the goal,
    # then its not as useful
    radGoalDistance = manhattanDistance(radPos, goalPos)
    # Obviously goal distance is important
    goalDistance = manhattanDistance(boatPos, goalPos)
    # We would rather be far away from the rad source
    radDistance = maxRadDist - manhattanDistance(boatPos, radPos)

    # Goal is more important if you are closer to the goal
    goalWeight = (goalDistance + 5.0)/goalDistance
    # Radiation is less important if the radiation and goal are far away
    # and less important if are far away
    radWeight = (radGoalDistance + 1.0)/(radGoalDistance + 2.0) * (goalDistance - 1.0)/goalDistance

    return goalWeight*goalDistance + radWeight*radDistance + goalBlocked + boatMobility
