"""
represents a node on the graph
"""
import Edge
from Point2D import Point2D


class Node:
    """
    this class represents a node on a graph
    """

    def __init__(self, id: int, pos: tuple):
        self._id = id
        self._pos = Point2D(pos)
        self._weight = 0
        self._inEdges = {}
        self._outEdges = {}

    def getID(self) -> int:
        return self._id

    def getPos(self) -> (float, float):
        return self._pos.getPosAsTuple()

    def getOutEdges(self):
        return self._outEdges

    def getInEdges(self):
        return self._inEdges

    def getWeight(self):
        return self._weight

    def set_weight(self, weight: float) -> None:
        self._weight = weight

    def add_in_edge(self, e: Edge) -> None:
        self._inEdges[e.getSrc()] = e.getWeight()

    def add_out_edge(self, e: Edge) -> None:
        self._outEdges[e.getDest()] = e.getWeight()
