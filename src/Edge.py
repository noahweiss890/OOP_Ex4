"""
represents an edge on the graph
"""


class Edge:

    def __init__(self, src: int, dest: int, weight: float):
        self._src = src
        self._dest = dest
        self._weight = weight

    def getSrc(self):
        return self._src

    def getDest(self):
        return self._dest

    def getWeight(self):
        return self._weight
