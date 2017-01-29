"""
Michael Harrington

This file contains path finder algorithms
"""

from Queue import Queue

"""
Search node class to hold a board state and other info
"""
class SearchNode():
    def __init__(self, boardState, parent, action):
        self.boardState = boardState
        self.parent = parent
        self.action = action

"""
Breadth Firtst Tree Search

Returns Success, Path :: Tuple(Bool, List)
"""
def BFTS(initialState, neighborGen, costCalc, isGoal):
    frontier = Queue()
    frontier.put( SearchNode(initialState, None, None) )
    while True:
        print 'None'
        if frontier.empty():
            return False, []
        selectNode = frontier.get()
        if isGoal(selectNode.boardState):
            return True, []
        for newNode, action in neighborGen(selectNode.boardState):
            frontier.put( SearchNode(newNode, selectNode, action) )

