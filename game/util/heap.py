"""
Michael Harrington

This file implements a Heap which is a wrapper over heapq
"""

from collections import defaultdict
import heapq

# We want to return this HeapNode class because we use the
# registry as a class variable but it needs to be specific
# to a Heap instance
def getHeapNodeClass():
    class HeapNode():
        registry = defaultdict(int)
    
        @classmethod
        def create(cls, el, val):
            heapNode = (val, cls.registry[el], el)
            cls.registry[el] += 1
            return heapNode
    return HeapNode

class Heap():
    def __init__(self):
        self.heap = []
        self.HeapNode = getHeapNodeClass()

    def push(self, el, val):
        newHeapNode = self.HeapNode.create(el, val)
        heapq.heappush(self.heap, newHeapNode)

    def pop(self):
        return heapq.heappop(self.heap)[-1]

    def __contains__(self, el):
        return el in self.HeapNode.registry

    def __nonzero__(self):
        return len(self.heap) != 0
