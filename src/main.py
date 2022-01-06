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

    info = (client.get_info())
    info_obj = json.loads(client.get_info())
    agent_amount = info_obj["GameServer"]["agents"]

    for i in range(agent_amount):
        client.add_agent("{\"id\":" + str(center) + "}")

    move_list = []
    EPSILON = 200

    # this commnad starts the server - the game is running now
    client.start()
    total_time = float(client.time_to_end())
    print(total_time)
    print((client.get_info()))

    while client.is_running() == 'true':

        # get agents from the server and create Agent objects from them
        agents_obj = json.loads(client.get_agents())
        for agent_obj in agents_obj["Agents"]:
            agent = agent_obj["Agent"]
            x, y, _ = agent["pos"].split(",")
            if agent["id"] in graphAlgo._agents:
                graphAlgo._agents[agent["id"]].update_agent(agent["value"], agent["src"], agent["dest"], agent["speed"], (float(x), float(y)))
            else:
                graphAlgo.add_agent(Agent(agent["id"], agent["value"], agent["src"], agent["dest"], agent["speed"], (float(x), float(y))))

        # get initial pokemons from the server and create Pokemon objects from them
        pokemons_json = client.get_pokemons()
        pokemons_obj = json.loads(pokemons_json)
        graphAlgo.reset_current_pokemons()
        for poke_obj in pokemons_obj["Pokemons"]:
            poke = poke_obj["Pokemon"]
            x, y, _ = poke["pos"].split(",")
            not_exists = 1
            for (p_pos), p_type in graphAlgo.getPokemons():
                if p_pos[0] == float(x) and p_pos[1] == float(y) and p_type == poke["type"]:
                    not_exists = 0
                    break
            if not_exists:
                new_poke = Pokemon(poke["value"], poke["type"], (float(x), float(y)), find_edge_with_pokemon(poke["type"], (float(x), float(y)), graph))
                graphAlgo.allocate_agent_to_pokemon(new_poke)
            graphAlgo.add_current_pokemon((float(x), float(y), poke["type"]))

        move_list += graphAlgo.call_move(int(client.time_to_end()))
        move_list.sort(reverse=True)

        # choose next edge
        allocate_list = graphAlgo.choosing_next_edge()
        for id, next_node in allocate_list:
            client.choose_next_edge('{"agent_id":'+str(id)+', "next_node_id":'+str(next_node)+'}')
        if len(allocate_list) > 0:
            print("ALLOCATE MOVE!")
            client.move()

        move_needed = False
        while move_list and int(client.time_to_end()) + EPSILON <= move_list[0]:
            move_list = move_list[1:]
            move_needed = True
        if move_needed:
            print("MOVE LIST MOVE!")
            client.move()

        info = (client.get_info())
        info_obj = json.loads(client.get_info())

        if play(graphAlgo, info_obj, int(client.time_to_end())):
            break

    # game over:
    client.stop()
    client.stop_connection()
    print((client.get_info()))
