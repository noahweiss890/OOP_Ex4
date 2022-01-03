"""
represents a node on the graph
"""
from src.Point2D import Point2D


class Node:
    def __init__(self, id: int, pos: tuple):
        self._id = id
        self._pos = Point2D(pos)

    def getID(self):
        return self._id

    def getPos(self):
        return self._pos
