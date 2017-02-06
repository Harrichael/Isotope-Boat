"""
Michael Harrington

This file contains path finder algorithms
"""

from collections import deque
from itertools import count

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
            if self.parent:
                self._path.extend(self.parent.path)
            self._path.append(self)

        return self._path

    # NOTE: Equal check is only based on board state!
    def __eq__(self, other):
        return self.boardState == other.boardState

    def __hash__(self):
        return hash(self.boardState)

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
Depth Limited Graph Search
"""
class DLGS(SearchSolver):
    def __init__(self, initialState, neighborGen, costCalc, isGoal, depthLimit):
        explored = set()
        frontier = deque()
        frontier.append( SearchNode(initialState, None, None, 0) )
        while True:
            if not frontier:
                self.searchNodePath = None
                break
            selectNode = frontier.pop()

            if isGoal(selectNode.boardState):
                self.searchNodePath = selectNode.path
                break
            explored.add(selectNode)
            if len(selectNode.path) > depthLimit:
                continue
            for newNode, action in neighborGen(selectNode.boardState):
                nodeCost = selectNode.pathCost + costCalc(newNode)
                newSearchNode = SearchNode(newNode, selectNode, action, nodeCost)
                if newSearchNode in frontier or newSearchNode in explored:
                    continue
                frontier.append(newSearchNode)

"""
Iterative Deepening Depth First Graph Search
"""
class IDDFGS(SearchSolver):
    def __init__(self, initialState, neighborGen, costCalc, isGoal):
        for depthLimit in count():
            solver = DLGS(initialState, neighborGen, costCalc, isGoal, depthLimit)
            if solver.pathFound:
                self.searchNodePath = solver.searchNodePath
                break

