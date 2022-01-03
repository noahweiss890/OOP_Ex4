"""
here we will run the program
"""
import json

from client import Client
from src.Graph import Graph
from src.GraphAlgos import find_edge_with_pokemon
from src.Pokemon import Pokemon

if __name__ == '__main__':

    # default port
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'

    client = Client()
    client.start_connection(HOST, PORT)

    graph_json = client.get_graph()
    graph_obj = json.loads(graph_json)
    graph = Graph(graph_obj)

    pokemons_json = client.get_pokemons()
    pokemons_obj = json.loads(pokemons_json)
    pokemons = []
    for poke in pokemons_obj["Pokemons"]:
        x, y, _ = poke["pos"].split(",")
        new_poke = Pokemon(float(poke["value"]), int(poke["type"]), (x, y), find_edge_with_pokemon(int(poke["type"]), (x, y), graph))

    agents_obj = json.loads(client.get_agents())
    agents = []
