"""
represents a pokemon
"""
import Edge
from Point2D import Point2D


class Pokemon:

    def __init__(self, value: float, type: int, pos: tuple, on_edge: Edge):
        self._value = value
        self._type = type
        self._pos = Point2D(pos)
        self._on_edge = on_edge

    def getValue(self) -> float:
        return self._value

    def getType(self) -> int:
        return self._type

    def getPos(self) -> Point2D:
        return self._pos

    def getOnEdge(self) -> Edge:
        return self._on_edge
