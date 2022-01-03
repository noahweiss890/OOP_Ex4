"""
represents an agent
"""


class Agent:

    def __init__(self, id: int, start: int):
        self._id = id
        self._src = start
        self._dest = -1
        self._future_calls = []
        self._future_moves = []

    def getID(self):
        return self._id

    def getSrc(self):
        return self._src

    def getDest(self):
        return self._dest

    def getFuture_calls(self):
        return self._future_calls

    def getFuture_moves(self):
        return self._future_moves
