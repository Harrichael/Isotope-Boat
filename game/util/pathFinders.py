"""
Michael Harrington

This file contains path finder algorithms
"""

from collections import deque

from timer import profile

"""
Search node class to hold a board state and other info
"""
class SearchNode():
    def __init__(self, boardState, parent, action, pathCost):
        self.boardState = boardState
        self.parent = parent
        self.action = action
        self.pathCost = pathCost
        # Derived attributes
        self._path = None

    @property
    def path(self):
        if not self._path:
            self._path = []
            node = self
            while node:
                self._path.insert(0, node)
                node = node.parent

        return self._path

"""
Base Search Class

Provides helper methods for use after completing search.
Subclasses expected to set searchNodePath to complete path.
"""
class SearchSolver():
    @property
    def pathFound(self):
        return bool(self.searchNodePath != None)

    @property
    def boardStatePath(self):
        return list(map(lambda n: n.boardState, self.searchNodePath))

    @property
    def actionPath(self):
        return list(map(lambda n: n.action, self.searchNodePath[1:]))

"""
Breadth First Tree Search
"""
class BFTS(SearchSolver):
    def __init__(self, initialState, neighborGen, costCalc, isGoal):
        frontier = deque()
        frontier.append( SearchNode(initialState, None, None, 0) )
        while True:
            if not frontier:
                self.searchNodePath = None
                break
            selectNode = frontier.popleft()

            if isGoal(selectNode.boardState):
                self.searchNodePath = selectNode.path
                break
            for newNode, action in neighborGen(selectNode.boardState):
                nodeCost = selectNode.pathCost + costCalc(newNode)
                frontier.append( SearchNode(newNode, selectNode, action, nodeCost) )

"""
Iterative Deepening Depth First Graph Search
"""
class IDDFGS(SearchSolver):
    def __init__(self, initialState, neighborGen, costCalc, isGoal):
        pass

