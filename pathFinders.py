"""
Michael Harrington

This file contains path finder algorithms
"""

from Queue import Queue

"""
Breadth Firtst Tree Search

Returns Success, Path :: Tuple(Bool, List)
"""
def BFTS(initialState, neighborGen, costCalc, isGoal):
    frontier = Queue()
    frontier.put(initialState)
    while True:
        if frontier.empty():
            return False, []
        selectNode = frontier.get()
        if isGoal(selectNode):
            return True, []
        for newNode in neighborGen(selectNode):
            frontier.put(newNode)

