"""
represents an agent
"""
import math

from typing import List
import Pokemon
import Node
from Point2D import Point2D
# from src import Pokemon, Node
# from src.Point2D import Point2D


def time_to_call_move(pokemon: Pokemon, src: Node, dest: Node) -> float:
    return (math.dist(src.getPos(), pokemon.getPos()) / math.dist(src.getPos(), dest.getPos())) * pokemon.getOnEdge.getWeight()


class Agent:

    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple):
        self._id = id
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        self._pos = Point2D(pos)
        self._future_calls = []
        self._future_moves = []

    def update_agent(self, value: float, src: int, dest: int, speed: float, pos: tuple):
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        self._pos = Point2D(pos)

    def getID(self) -> int:
        return self._id

    def getValue(self) -> float:
        return self._value

    def setValue(self, value: float) -> None:
        self._value = value

    def getSrc(self) -> int:
        return self._src

    def setSrc(self, src: int) -> None:
        self._src = src

    def getDest(self) -> int:
        return self._dest

    def setDest(self, dest: int) -> None:
        self._dest = dest

    def getSpeed(self) -> float:
        return self._speed

    def setSpeed(self, speed: float) -> None:
        self._speed = speed

    def getPos(self) -> Point2D:
        return self._pos

    def setPos(self, pos: Point2D) -> None:
        self._pos = pos

    def getFuture_calls(self) -> list:
        return self._future_calls

    def getFuture_moves(self) -> list:
        return self._future_moves

    def add_pokemon(self, pokemon: Pokemon, path: List[int], time: float, ttl: float, src: Node, dest: Node) -> None:
        new_path = []
        for i in path[:-1]:
            new_path.append((i, -1))
        if self._future_calls == []:
            self._future_calls = new_path
        else:
            self._future_calls += new_path[1:]
        self._future_calls.append((pokemon.getOnEdge().getSrc(), pokemon.getOnEdge().getDest()))
        self._future_moves.append(ttl - (time + time_to_call_move(pokemon, src, dest)) / self._speed)
