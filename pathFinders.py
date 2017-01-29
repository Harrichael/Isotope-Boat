"""
Michael Harrington

This file contains path finder algorithms
"""

from Queue import Queue

"""
Search node class to hold a board state and other info
"""
class SearchNode():
    def __init__(self, boardState, parent):
        self.boardState = boardState
        self.parent = parent

"""
Breadth Firtst Tree Search

Returns Success, Path :: Tuple(Bool, List)
"""
def BFTS(initialState, neighborGen, costCalc, isGoal):
    frontier = Queue()
    frontier.put( SearchNode(initialState, None) )
    while True:
        if frontier.empty():
            return False, []
        selectNode = frontier.get()
        if isGoal(selectNode.boardState):
            return True, []
        for newNode in neighborGen(selectNode.boardState):
            frontier.put( SearchNode(newNode, selectNode) )

