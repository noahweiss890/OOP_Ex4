"""
represents an agent
"""

from typing import List
import Pokemon
from Point2D import Point2D


class Agent:

    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple):
        self._id = id
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        self._pos = Point2D(pos)
        self._future_calls = []
        self._pokemons = []

    def update_agent(self, value: float, src: int, dest: int, speed: float, pos: tuple):
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        self._pos.updatePos(pos)

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

    def getPos(self) -> (float, float):
        return self._pos.getPosAsTuple()

    def setPos(self, pos: Point2D) -> None:
        self._pos = pos

    def getFuture_calls(self) -> list:
        return self._future_calls

    def setFuture_calls(self, path: list):
        self._future_calls = path

    def add_pokemon(self, pokemon: Pokemon, path: List[int]) -> None:
        new_path = []
        for i in path[:-1]:
            new_path.append([i, -1])
        if not self._future_calls:
            self._future_calls = new_path[1:]
        else:
            self._future_calls += new_path[1:]
        self._future_calls.append([pokemon.getOnEdge().getSrc(), pokemon.getOnEdge().getDest()])
        self._pokemons.append(pokemon)

    def add_pokemon_on_the_way(self, pokemon: Pokemon) -> None:
        self._pokemons.append(pokemon)
        if self._dest == pokemon.getOnEdge().getSrc() and self._future_calls[0][0] == pokemon.getOnEdge().getDest() and self._future_calls[0][1] == -1:
            self._future_calls[0] = [-1, self._future_calls[0][0]]
            return
        else:
            for i, call in enumerate(self._future_calls):
                if call[0] == pokemon.getOnEdge().getSrc() and call[1] == -1 and self._future_calls[i+1][0] == pokemon.getOnEdge().getDest() and self._future_calls[i+1][1] == -1:
                    call[1] = pokemon.getOnEdge().getDest()
                    self._future_calls.pop(i+1)
                    return
                elif call[0] == pokemon.getOnEdge().getSrc() and call[1] == -1 and self._future_calls[i+1][0] == pokemon.getOnEdge().getDest():
                    call[1] = pokemon.getOnEdge().getDest()
                    return

    def delete_pokemon(self, pokemon: Pokemon) -> None:
        self._pokemons.remove(pokemon)

    def getPokemons(self) -> list:
        return self._pokemons
