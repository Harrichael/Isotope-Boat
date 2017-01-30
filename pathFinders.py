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

    def createPath(self):
        path = []
        node = self
        while node:
            path.insert(0, node)
            node = node.parent
        return path

"""
Breadth Firtst Tree Search
"""
class BFTS():
    def __init__(self, initialState, neighborGen, costCalc, isGoal):
        frontier = Queue()
        frontier.put( SearchNode(initialState, None, None) )
        while True:
            if frontier.empty():
                self.searchNodePath = None
                break
            selectNode = frontier.get()
            if isGoal(selectNode.boardState):
                self.searchNodePath = selectNode.createPath()
                break
            for newNode, action in neighborGen(selectNode.boardState):
                frontier.put( SearchNode(newNode, selectNode, action) )

    @property
    def pathFound(self):
        return bool(self.searchNodePath != None)

    @property
    def boardStatePath(self):
        return map(lambda n: n.boardState, self.searchNodePath)

    @property
    def actionPath(self):
        return map(lambda n: n.action, self.searchNodePath[1:])

