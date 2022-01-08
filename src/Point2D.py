class Point2D:
    """
    this class represents a point on a graph
    """

    def __init__(self, pos: tuple):
        self._x, self._y = pos

    def getX(self) -> float:
        return self._x

    def getY(self) -> float:
        return self._y

    def getPosAsTuple(self) -> (float, float):
        """
        :return: a tuple of the x and y coordinates
        """
        return self._x, self._y

    def updatePos(self, pos: tuple) -> None:
        """
        sets its coordinates to be the given coordinates
        :param pos: tuple of x and y coordinates
        """
        self._x, self._y = pos
