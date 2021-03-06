"""
Michael Harrington

This file implements a Heap which is a wrapper over heapq
"""

from collections import defaultdict
import heapq
from random import randint

# We want to return this HeapNode class because we use the
# registry as a class variable but it needs to be specific
# to a Heap instance
def getHeapNodeClass():
    class HeapNode():
        elCounts = defaultdict(int)
        registry = defaultdict(list)

        @classmethod
        def create(cls, el, val):
            orVal = cls.elCounts[el]
            # This tuple is used for ordering, el will never be compared
            # The second tuple item is used to randomly prioritize earlier els when tied
            # The third tuple item ensures that el will not need to be compared
            heapNode = (val, randint(orVal/2, orVal), orVal, el)
            cls.elCounts[el] += 1
            cls.registry[el].append(heapNode)
            return heapNode

    return HeapNode

class Heap():
    def __init__(self):
        self.heap = []
        self.HeapNode = getHeapNodeClass()

    def push(self, el, val):
        newHeapNode = self.HeapNode.create(el, val)
        heapq.heappush(self.heap, newHeapNode)

    def uniquePush(self, el, val):
        if el in self.HeapNode.registry:
            if val < self.HeapNode.registry[el][0][0]:
                self.heap.remove(self.HeapNode.registry[el][0])
                self.HeapNode.registry[el] = []
                self.HeapNode.elCounts[el] = 0
                
            else:
                # El is present with lower val
                return
        self.push(el, val)

    def pop(self):
        return heapq.heappop(self.heap)[-1]

    def __contains__(self, el):
        return el in self.HeapNode.registry

    def __nonzero__(self):
        return len(self.heap) != 0

