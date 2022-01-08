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

    center = graphAlgo.centerPoint()  # for making all of the agents start at the center node of the graph

    info = (client.get_info())
    info_obj = json.loads(client.get_info())
    agent_amount = info_obj["GameServer"]["agents"]  # finding out from the server how many agents there are in this case

    for i in range(agent_amount):
        client.add_agent("{\"id\":" + str(center) + "}")  # create an agent

    move_list = []
    EPSILON = 3  # to be used for knowing when to call move

    # this commnad starts the server - the game is running now
    client.start()
    total_time = float(client.time_to_end())  # get the total time the game will go on for

    # only stop if the server isn't running anymore, the tim eis under a tenth of a second, or if the moves is bigger than the allowed amount
    while client.is_running() == 'true' and float(client.time_to_end()) > 100 and info_obj["GameServer"]["moves"] < 10 * (total_time // 1000):

        # get agents from the server and create Agent objects from them
        agents_obj = json.loads(client.get_agents())
        for agent_obj in agents_obj["Agents"]:
            agent = agent_obj["Agent"]
            x, y, _ = agent["pos"].split(",")
            if agent["id"] in graphAlgo._agents:  # check if this agent already exists, if he doesnt then create him, but if he does than update his info
                graphAlgo._agents[agent["id"]].update_agent(agent["value"], agent["src"], agent["dest"], agent["speed"], (float(x), float(y)))
            else:
                graphAlgo.add_agent(Agent(agent["id"], agent["value"], agent["src"], agent["dest"], agent["speed"], (float(x), float(y))))

        # get pokemons from the server and create Pokemon objects from them
        pokemons_json = client.get_pokemons()
        pokemons_obj = json.loads(pokemons_json)
        graphAlgo.reset_current_pokemons()  # empty the old list of pokemon so it can be updated
        for poke_obj in pokemons_obj["Pokemons"]:  # go through all of the pokemons
            poke = poke_obj["Pokemon"]
            x, y, _ = poke["pos"].split(",")  # get the x and y coordinates of the pokemon (ignore z coordinate)
            not_exists = 1
            for (p_pos), p_type in graphAlgo.getPokemons():
                if p_pos[0] == float(x) and p_pos[1] == float(y) and p_type == poke["type"]:  # check if this pokemon was already allocated to an agent
                    not_exists = 0
                    break
            if not_exists:  # if the pokemon is new, then allocate it to an agent
                new_poke = Pokemon(poke["value"], poke["type"], (float(x), float(y)), find_edge_with_pokemon(poke["type"], (float(x), float(y)), graph))  # create a Pokemon object
                graphAlgo.allocate_agent_to_pokemon(new_poke)  # allocate the pokemon to an agent
            graphAlgo.add_current_pokemon((float(x), float(y), poke["type"], poke["value"]))  # add the pokemon to the current pokemon list

        move_list += graphAlgo.call_move(float(client.time_to_end()))  # get the list of moves that are needed to be called
        move_list.sort(reverse=True)  # sort the list

        # choose next edge
        allocate_list = graphAlgo.choosing_next_edge()  # gets a list of all the next edges needed to be called for all of the agents
        for id, next_node in allocate_list:
            client.choose_next_edge('{"agent_id":'+str(id)+', "next_node_id":'+str(next_node)+'}')

        move_needed = False
        while move_list and float(client.time_to_end()) + EPSILON <= move_list[0]:  # goes through the move list and checks if it is time for a move to be called
            move_list = move_list[1:]  # remove this call from the move list
            move_needed = True
        if move_needed:  # if move needs to be called
            client.move()  # call move

        info = (client.get_info())  # get the game info from the server
        info_obj = json.loads(client.get_info())  # turn the info into an object

        if play(graphAlgo, info_obj, int(client.time_to_end())):  # run the GUI, if it returns True then the user has selected to stop the game
            break

    # game over:
    print(client.get_info())
    client.stop_connection()  # stop the connection with server
    # client.stop()
