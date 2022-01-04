"""
represnts a 2D point on the graph
"""


class Point2D:

    def __init__(self, pos: tuple):
        self._x, self._y = pos

    def getX(self) -> float:
        return self._x

    def getY(self) -> float:
        return self._y
