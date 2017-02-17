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

def explorativeHeuristic(boardState):
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
    # We should reward a position with low number of obstacles between goal and boat
    goalTrack = set()
    xOffset = 1 if boatPos.x < goalPos.x else -1
    yOffset = 1 if boatPos.y < goalPos.y else -1
    for x in range(boatPos.x, goalPos.x + xOffset, xOffset):
        for y in range(boatPos.y, goalPos.y + yOffset, yOffset):
            goalTrack.add(Point(x, y))
    obstacleObjs = boardState.alligators + boardState.turtles + boardState.trees
    obstaclePoints = set(chain(*[obst.space for obst in obstacleObjs]))
    obstacleCost = len(goalTrack.intersection(obstaclePoints))

    # Goal is more important if you are closer to the goal
    goalWeight = (goalDistance + 5.0)/goalDistance
    # Radiation is less important if the radiation and goal are far away
    # and less important if are far away
    radWeight = (radGoalDistance + 1.0)/(radGoalDistance + 2.0) * (goalDistance - 1.0)/goalDistance

    return goalWeight*goalDistance + radWeight*radDistance + goalBlocked + boatMobility + obstacleCost

def createGreedyHeuristic(initialBoardState):
    goalPos = initialBoardState.goal.pos
    boardPos = initialBoardState.board.pos
    def greedyHeuristic(boardState):
        # If goal is made, give it best priority!
        if boardState.boat.collision(boardState.goal):
            return 0
    
        # Lets make some helper values
        boatPos = boardState.boat.cardRay.pos
        boatFrontPos = rayToPointList(boardState.boat.cardRay, boardState.boat.objLength)[-1]
    
        # Obviously goal distance is important
        goalDist = min( manhattanDistance(boatPos, goalPos),
                        manhattanDistance(boatFrontPos, goalPos),
                      )
    
        # We should reward a position with low number of obstacles between goal and boat
        minX = min(boatPos.x, goalPos.x, boatFrontPos.x)
        maxX = max(boatPos.x, goalPos.x, boatFrontPos.x)
        minY = min(boatPos.y, goalPos.y, boatFrontPos.y)
        maxY = max(boatPos.y, goalPos.y, boatFrontPos.y)
        goalTrack = set()
        for x in range(minX, maxX+1):
            for y in range(minY, maxY+1):
                goalTrack.add(Point(x, y))
        obstacleObjs = boardState.alligators + boardState.turtles + boardState.trees
        obstaclePoints = set(chain(*[obst.space for obst in obstacleObjs]))
        obstacleCost = len(goalTrack.intersection(obstaclePoints))
    
        return goalDist + obstacleCost

    return greedyHeuristic
