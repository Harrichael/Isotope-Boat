"""
Michael Harrington

This file provides heuristics for path finders
"""

from itertools import chain

from game.gameRules import MapEntity, Moves
from game.util.cartMath import manhattanDistance, rayToPointList, Point, Cardinal

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

"""
We are just discovering what we can do with this heuristic
"""
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

"""
This heuristic is for greedy searching
"""
def createGreedyHeuristic(initialBoardState):
    goalPos = initialBoardState.goal.pos
    boardPos = initialBoardState.board.pos
    def greedyHeuristic(boardState):
        # If goal is made, give it best priority!
        if boardState.boat.collision(boardState.goal):
            return 0
    
        # Lets make some helper values
        boatCardRay = boardState.boat.cardRay
        boatPos = boatCardRay.pos
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

        if (maxX - minX) > (maxY - minY):
            orCostDict = { Cardinal.left:  0 if minX == goalPos.x else 4,
                           Cardinal.right: 0 if maxX == goalPos.x else 4,
                           Cardinal.up:    1,
                           Cardinal.down:  1,
                         }
        else:
            orCostDict = { Cardinal.up:    0 if minY == goalPos.y else 4,
                           Cardinal.down:  0 if maxY == goalPos.y else 4,
                           Cardinal.left:  1,
                           Cardinal.right: 1,
                         }
            
        orientationCost = orCostDict[boatCardRay.cardDir]

        return goalDist + obstacleCost + orientationCost

    return greedyHeuristic

"""
Smart heuristic that gives a decent cost estimation even for A-Star searches
"""
def createSmartHeuristic(initialBoardState):
    goalPos = initialBoardState.goal.pos
    boardPos = initialBoardState.board.pos
    def smartHeuristic(boardState):
        # If goal is made, give it best priority!
        if boardState.boat.collision(boardState.goal):
            return 0
    
        # Lets make some helper values
        boatCardRay = boardState.boat.cardRay
        boatPos = boatCardRay.pos
        boatFrontPos = rayToPointList(boardState.boat.cardRay, boardState.boat.objLength)[-1]
        radSrc = boardState.radSrc
    
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

        orCostDict = { Cardinal.left:  0,
                       Cardinal.right: 0,
                       Cardinal.up:    0,
                       Cardinal.down:  0,
                     }
        if maxX == goalPos.x:
            orCostDict[Cardinal.left] = 1
        if minX == goalPos.x:
            orCostDict[Cardinal.right] = 1
        if maxY == goalPos.y:
            orCostDict[Cardinal.up] = 1
        if minY == goalPos.y:
            orCostDict[Cardinal.down] = 1
        orientationCost = orCostDict[boatCardRay.cardDir]

        minRadCost = 2*min(radSrc.rads(p) for p in goalTrack) + radSrc.decayFactor

        return (goalDist + obstacleCost + orientationCost) * minRadCost

    return smartHeuristic

"""
Admissable heuristic that gives optimal paths with A-Star TS
"""
def createAdmissableHeuristic(initialBoardState):
    goalPos = initialBoardState.goal.pos
    boardPos = initialBoardState.board.pos
    radSrc = initialBoardState.radSrc
    minRadCost = 2*min([radSrc.rads(Point(x, y)) 
                        for x in range(boardPos.x)
                            for y in range(boardPos.y)]
                      ) + radSrc.decayFactor
    def admissableHeuristic(boardState):
        # If goal is made, give it best priority!
        if boardState.boat.collision(boardState.goal):
            return 0

        # Lets make some helper values
        boatCardRay = boardState.boat.cardRay
        boatPos = boatCardRay.pos
        boatFrontPos = rayToPointList(boardState.boat.cardRay, boardState.boat.objLength)[-1]
        goalBackDist = manhattanDistance(boatPos, goalPos)
        goalFrontDist = manhattanDistance(boatPos, goalPos)
        obstacleObjs = boardState.alligators + boardState.turtles + boardState.trees
        obstaclePoints = set(chain(*[obst.space for obst in obstacleObjs]))
        minX = min(boatPos.x, goalPos.x, boatFrontPos.x)
        maxX = max(boatPos.x, goalPos.x, boatFrontPos.x)
        minY = min(boatPos.y, goalPos.y, boatFrontPos.y)
        maxY = max(boatPos.y, goalPos.y, boatFrontPos.y)

        # We cannot overestimate costs in the case of this state is adjacent to a goal state
        # Remember, when moving to a goal you incur no radiation cost
        if goalFrontDist == 1 and (boatPos.x == goalPos.x or boatPos.y == goalPos.y):
            # We are inline from the goal and one away, but is goal clear?
            if goalPos not in obstaclePoints:
                return 0
        elif goalBackDist == 1 and boatFrontPos.x != goalPos.x and boatFrontPos.y != goalPos.y:
            # We may be able to twist into the goal, if certain space and goal is clear
            if goalPos not in obstaclePoints:
                # One of these two points in the boatPos,
                # the other is the space the boat rotates through
                p1 = Point(goalPos.x, boatFrontPos.y)
                p2 = Point(boatFrontPos.x, goalPos.y)
                if p1 not in obstaclePoints and p2 not in obstaclePoints:
                    return 0

        orCostDict = { Cardinal.left:  0,
                       Cardinal.right: 0,
                       Cardinal.up:    0,
                       Cardinal.down:  0,
                     }
        if maxX == goalPos.x:
            orCostDict[Cardinal.left] = 1
        if minX == goalPos.x:
            orCostDict[Cardinal.right] = 1
        if maxY == goalPos.y:
            orCostDict[Cardinal.up] = 1
        if minY == goalPos.y:
            orCostDict[Cardinal.down] = 1
        orientationCost = orCostDict[boatCardRay.cardDir]

        # Obviously goal distance is important
        goalDist = min(goalBackDist, goalFrontDist)

        return (goalDist + orientationCost) * minRadCost

    return admissableHeuristic
"""
Consistent heuristic that gives optimal paths with A-Star GS
"""
def createConsistentHeuristic(initialBoardState):
    goalPos = initialBoardState.goal.pos
    boardPos = initialBoardState.board.pos
    radSrc = initialBoardState.radSrc
    minRadCost = 2*min([radSrc.rads(Point(x, y)) 
                        for x in range(boardPos.x)
                            for y in range(boardPos.y)]
                      ) + radSrc.decayFactor
    def consistentHeuristic(boardState):
        # If goal is made, give it best priority!
        if boardState.boat.collision(boardState.goal):
            return 0

        # Lets make some helper values
        boatPos = boardState.boat.cardRay.pos
        boatFrontPos = rayToPointList(boardState.boat.cardRay, boardState.boat.objLength)[-1]
        goalBackDist = manhattanDistance(boatPos, goalPos)
        goalFrontDist = manhattanDistance(boatPos, goalPos)
        obstacleObjs = boardState.alligators + boardState.turtles + boardState.trees
        obstaclePoints = set(chain(*[obst.space for obst in obstacleObjs]))

        # We cannot overestimate costs in the case of this state is adjacent to a goal state
        # Remember, when moving to a goal you incur no radiation cost
        if goalFrontDist == 1 and (boatPos.x == goalPos.x or boatPos.y == goalPos.y):
            # We are inline from the goal and one away, but is goal clear?
            if goalPos not in obstaclePoints:
                return 0
        elif goalBackDist == 1 and boatFrontPos.x != goalPos.x and boatFrontPos.y != goalPos.y:
            # We may be able to twist into the goal, if certain space and goal is clear
            if goalPos not in obstaclePoints:
                # One of these two points in the boatPos,
                # the other is the space the boat rotates through
                p1 = Point(goalPos.x, boatFrontPos.y)
                p2 = Point(boatFrontPos.x, goalPos.y)
                if p1 not in obstaclePoints and p2 not in obstaclePoints:
                    return 0

        # Obviously goal distance is important
        goalDist = min(goalBackDist, goalFrontDist)

        return goalDist * minRadCost

    return consistentHeuristic
