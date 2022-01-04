"""
represents a node on the graph
"""
from src import Edge
from src.Point2D import Point2D


class Node:
    def __init__(self, id: int, pos: tuple):
        self._id = id
        self._pos = Point2D(pos)
        self.weight = 0
        self.inEdges = {}
        self.outEdges = {}

    def getID(self) -> int:
        return self._id

    def getPos(self) -> Point2D:
        return self._pos

    def set_weight(self, weight: float) -> None:
        self.weight = weight

    def add_in_edge(self, e: Edge) -> None:
        self.inEdges[e.src] = e.weight

    def add_out_edge(self, e: Edge) -> None:
        self.outEdges[e.dest] = e.weight
