from unittest import TestCase

from src.Edge import Edge
from src.Pokemon import Pokemon


class TestPokemon(TestCase):
    def test_get_value(self):
        edge = Edge(3,6,10)
        pokemon = Pokemon(5, 1, (22,23), edge)
        self.assertEqual(pokemon.getValue(), 5)

    def test_get_type(self):
        edge = Edge(3,6,10)
        pokemon = Pokemon(5, 1, (22,23), edge)
        self.assertEqual(pokemon.getType(), 1)

    def test_get_pos(self):
        edge = Edge(3,6,10)
        pokemon = Pokemon(5, 1, (22,23), edge)
        self.assertEqual(pokemon.getPos(), (22,23))

    def test_get_on_edge(self):
        edge = Edge(3,6,10)
        pokemon = Pokemon(5, 1, (22,23), edge)
        self.assertEqual(pokemon.getOnEdge(), edge)
