"""
represents a pokemon
"""
from src import Edge
from src.Point2D import Point2D


class Pokemon:

    def __init__(self, value: float, type: int, pos: tuple, on_edge: Edge):
        self._value = value
        self._type = type
        self._pos = Point2D(pos)
        self._on_edge = on_edge

