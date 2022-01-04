"""
here we will run the program
"""
import json

from client import Client
from Agent import Agent
from Graph import Graph
from GraphAlgos import GraphAlgos, find_edge_with_pokemon
from Pokemon import Pokemon
from PokemonGUI import play

if __name__ == '__main__':

    # default port
    PORT = 6666
    # server host (default localhost 127.0.0.1)
    HOST = '127.0.0.1'

    # open connection to server
    client = Client()
    client.start_connection(HOST, PORT)

    # get graph from the server
    graph_json = client.get_graph()
    graph_obj = json.loads(graph_json)
    graph = Graph(graph_obj)

    graphAlgo = GraphAlgos(graph)

    center, _ = graphAlgo.centerPoint()
    client.add_agent("{\"id\":" + str(center) + "}")

    # this commnad starts the server - the game is running now
    client.start()

    while client.is_running() == 'true':

        # get agents from the server and create Agent objects from them
        agents_obj = json.loads(client.get_agents())
        for agent_obj in agents_obj["Agents"]:
            agent = agent_obj["Agent"]
            x, y, _ = agent["pos"].split(",")
            new_agent = Agent(int(agent["id"]), float(agent["value"]), int(agent["src"]), int(agent["dest"]), float(agent["speed"]), (float(x), float(y)))
            if int(agent["id"]) in graphAlgo._agents:
                graphAlgo._agents[int(agent["id"])].update_agent(float(agent["value"]), int(agent["src"]), int(agent["dest"]), float(agent["speed"]), (float(x), float(y)))
            else:
                graphAlgo.add_agent(new_agent)

        # get initial pokemons from the server and create Pokemon objects from them
        pokemons_json = client.get_pokemons()
        pokemons_obj = json.loads(pokemons_json)
        for poke_obj in pokemons_obj["Pokemons"]:
            poke = poke_obj["Pokemon"]
            x, y, _ = poke["pos"].split(",")
            new_poke = Pokemon(float(poke["value"]), int(poke["type"]), (float(x), float(y)), find_edge_with_pokemon(int(poke["type"]), (float(x), float(y)), graph))
            graphAlgo.allocate_agent_to_pokemon(new_poke, float(client.time_to_end()))
            graphAlgo.add_pokemon(new_poke)

        # choose next edge
        allocate_list = graphAlgo.choosing_next_edge()
        for id, next_node in allocate_list:
            client.choose_next_edge('{"agent_id":'+str(id)+', "next_node_id":'+str(next_node)+'}')

        play(graphAlgo)

    # game over:
    client.stop_connection()
