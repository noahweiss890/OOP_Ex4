from unittest import TestCase

from src.Agent import Agent
from src.Edge import Edge
from src.Point2D import Point2D
from src.Pokemon import Pokemon


class TestAgent(TestCase):

    def test_update_agent(self):
        agent = Agent(0, 0.0, 0, -1, 1.0, (35.20319591121872,32.1031462))
        agent.update_agent(100.0, 3, 4, 2.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getValue(), 100.0)
        self.assertEqual(agent.getSrc(), 3)
        self.assertEqual(agent.getDest(), 4)

    def test_getID(self):
        agent = Agent(0, 0.0, 0, -1, 1.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getID(), 0)

    def test_getValue(self):
        agent = Agent(0, 0.0, 0, -1, 1.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getValue(), 0.0)

    def test_setValue(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        agent.setValue(21)
        self.assertEqual(agent.getValue(), 21)

    def test_getSrc(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getSrc(), 6)

    def test_setSrc(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        agent.setSrc(21)
        self.assertEqual(agent.getSrc(), 21)

    def test_getDest(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getDest(), 5)

    def test_setDest(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        agent.setDest(21)
        self.assertEqual(agent.getDest(), 21)

    def test_getSpeed(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getSpeed(), 1)

    def test_setSpeed(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        agent.setSpeed(21)
        self.assertEqual(agent.getSpeed(), 21)

    def test_getpos(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getPos(), (35.20319591121872,32.1031462))

    def test_setpos(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        agent.setPos(Point2D((34,36)))
        self.assertEqual(agent.getPos(), (34,36))

    def test_getFuture_calls(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        self.assertEqual(agent.getFuture_calls(), [])

    def test_setFuture_calls(self):
        pass

    def test_delete_pokemon(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        pokemon = Pokemon(6.0, 1, (35.20539663533063,32.10283686555705), Edge(2,3,5))
        agent.add_pokemon(pokemon, [0,1,2])
        agent.delete_pokemon(pokemon)
        self.assertEqual(agent.getPokemons(), [])

    def test_getPokemons(self):
        agent = Agent(0, 0.0, 6, 5, 1.0, (35.20319591121872,32.1031462))
        pokemon = Pokemon(6.0, 1, (35.20539663533063,32.10283686555705), Edge(2,3,5))
        agent.add_pokemon(pokemon, [0,1,2])
        self.assertEqual(agent.getPokemons(), [pokemon])

    def test_add_pokemon(self):
        agent = Agent(0, 0.0, 0, -1, 1.0, (35.20319591121872,32.1031462))
        pokemon = Pokemon(6.0, 1, (35.20539663533063,32.10283686555705), Edge(2,3,5))
        agent.add_pokemon(pokemon, [0,1,2])
        self.assertEqual(agent.getFuture_calls(), [[1, -1], [2, 3]])
        self.assertEqual(agent.getPokemons(), [pokemon])

    def test_add_pokemon_on_the_way(self):
        agent = Agent(0, 0.0, 0, -1, 1.0, (35.20319591121872,32.1031462))
        pokemon1 = Pokemon(6.0, 1, (35.20539663533063,32.10283686555705), Edge(4,5,5))
        agent.add_pokemon(pokemon1, [0,1,2,3,4])
        pokemon2 = Pokemon(16.0, 1, (35.20539663533063,32.10283686555705), Edge(2,3,5))
        agent.add_pokemon_on_the_way(pokemon2)
        self.assertEqual(agent.getFuture_calls(), [[1, -1], [2, 3], [4, 5]])
        self.assertEqual(agent.getPokemons(), [pokemon1, pokemon2])
