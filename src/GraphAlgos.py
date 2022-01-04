"""
class that holds all of the functions that will be used for graphs
"""
import heapq
import math

from typing import List

from client import Client
from src import Pokemon, Point2D, Agent
from src.Graph import Graph

EPSILON = 0.001


def find_edge_with_pokemon(type: int, pos: Point2D, graph: Graph):
    for e in graph.get_all_e():
        if type > 0 and e.getSrc() < e.getDest():
            if math.dist(graph.get_all_v().get(e.getSrc()).getPos(), pos) + math.dist(pos, graph.get_all_v().get(e.getDest()).getPos()) < math.dist(graph.get_all_v().get(e.getSrc()).getPos(), graph.get_all_v().get(e.getDest()).getPos()) + EPSILON:
                return e
    print("POKEMON NOT ON GRAPH!")


class GraphAlgos:

    def __init__(self, graph_json: dict, agents: dict):
        self.graph = Graph(graph_json)
        self.agents = agents

    def getGraph(self):
        return self.graph

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
        global node_weight
        if id1 not in self.graph.get_all_v() or id2 not in self.graph.get_all_v():  # If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
            return float('inf'), []
        if id1 == id2:  # if both ids entered are the same, the path is just the node itself and the cost is zero
            return 0.0, [id1]
        dijkstra = {i: float('inf') for i in self.graph.get_all_v()}  # turning all "weights" to infinity
        dijkstra[id1] = 0  # turns start node's "weight" to 0
        pq = []
        prev = {}
        for n in self.graph.get_all_v():  # assign all nodes prev = None
            prev[n] = None
            if n != id1:
                heapq.heappush(pq, (float('inf'), n))  # push into heapified list pq
            else:
                heapq.heappush(pq, (0, n))
        while len(pq) != 0:
            heapq.heapify(pq)
            node_weight, i = heapq.heappop(pq)
            if dijkstra[i] == float('inf'):  # if popping a node who's weight is infinity, no path exists
                return float('inf'), []
            if i == id2:  # found path
                break
            for dest, w in self.graph.all_out_edges_of_node(i).items():  # all neighbors of i
                if dijkstra[dest] > dijkstra[i] + w:
                    pq.remove((dijkstra[dest], dest))  # removes id from pq
                    dijkstra[dest] = dijkstra[i] + w  # relaxes
                    prev[dest] = i  # updates prev
                    heapq.heappush(pq, (dijkstra[dest], dest))  # push id back into pq with new weight
        temp = id2
        short_path = [temp]
        while prev[temp] is not None:  # create list path
            short_path.insert(0, prev[temp])
            temp = prev[temp]
        return node_weight, short_path

    def TSP(self, src: int, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list. Uses helper function closestNodeFinder to
        locate which node in the list is closest to the current node :param node_lst: A list of nodes id's :return: A
        list of the nodes id's in the path, and the overall distance
        """
        if len(node_lst) == 1:  # one value in list, return just itself and cost is zero
            return node_lst[0], 0.0
        path = [src]
        cities = node_lst.copy()
        cost = 0.0
        curr = src
        while True:
            cities.remove(curr)  # remove curr from cities before sending to helper function in order to actually
            # find closest node not including the node itself
            if len(cities) == 1:  # only one left
                break
            closest_node_path = self._closestNodeFinder(cities, curr)  # returns the shorest path to the closest
            # node and the price is cost to get there
            path += closest_node_path[0][1:]  # add path except for first value because already added to path
            cost += closest_node_path[1]  # update cost
            curr = closest_node_path[0][-1]  # curr now equals what was the next closest node
        closest_last = self.shortest_path(curr, cities[0])  # finds shortest path from last closest node to last
        # value in cities
        path += closest_last[1][1:]  # adds to path
        cost += closest_last[0]  # updates cost
        return path, cost

    def _closestNodeFinder(self, n_list: List[int], curr_node: int) -> (List[int], float):
        """
        TSP helper function. finds the closest node in the given list to the curr_node
        @param n_list: List of cities to visit
        @param curr_node: starter node
        @return: returns the shortest path from curr_node to closest node in list and the cost to get there
        """
        global curr, node_w
        path_w = 0.0
        dijkstra = {i: float('inf') for i in self.graph.get_all_v()}  # turning all "weights" to infinity
        dijkstra[curr_node] = 0  # turns "weight" of starter node 0
        pq = []
        prev = {}
        for n in self.graph.get_all_v():
            prev[n] = None
            if n != curr_node:
                heapq.heappush(pq, (float('inf'), n)) # push into heapified list pq
            else:
                heapq.heappush(pq, (0, n))  # push into heapified list pq
        while len(pq) != 0:
            heapq.heapify(pq)
            node_w, curr = heapq.heappop(pq)  # pops lowest weighted value in pq
            if dijkstra[curr] == float('inf'):  # if popping a node who's weight is infinity, no path exists
                return [], -1
            if curr in n_list:  # found value in list
                break
            for neighbor, w in self.graph.all_out_edges_of_node(curr).items():  # check neighbors
                if dijkstra[neighbor] > dijkstra[curr] + w:
                    pq.remove((dijkstra[neighbor], neighbor))  # removes id from pq
                    dijkstra[neighbor] = dijkstra[curr] + w  #relaxes
                    prev[neighbor] = curr  # updates prev
                    heapq.heappush(pq, (dijkstra[neighbor], neighbor))  # push id back into pq with new weight
        if len(pq) == 0:  # got to end of list and did not find a closest node
            return [], -1
        temp_node = curr
        path_w += node_w
        dij_path = [temp_node]
        while prev[temp_node] is not None:
            dij_path.insert(0, prev[temp_node])
            temp_node = prev[temp_node]
        return dij_path, node_w

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node. This function uses a helper function
        eccentricity.
        return: The nodes id, min-maximum distance
        """
        min_weight = float('inf')
        center_node = None
        for n in self.graph.get_all_v():  # go through all nodes in the graph
            ecc_w = self.eccentricity(n, min_weight)  # find out what the eccentricity of the node is
            if ecc_w == float('inf'):  # if the ecc is inf then the graph is not connected and therefore there is no center
                return None, float('inf')
            if ecc_w != -1 and ecc_w < min_weight:  # if we found a shorter ecc, if the ecc is -1 then the ecc is higher than the current min_weight and stopped early
                min_weight = ecc_w
                center_node = n
        return center_node, min_weight

    def eccentricity(self, node: int, minWeight: float) -> float:
        """
        This is a helper function for centerPoint to find out what the eccentricity from the given node
        :param node: id of node
        :param minWeight: the minWeight that has been found so far
        :return: the eccentricity of the graph from the given node
        """
        dijkstra = {i: float('inf') for i in self.graph.get_all_v()}  # to hold all of the weights between each node to the given node
        dijkstra[node] = 0  # weight is 0 to itself
        pq = []  # priority queue
        for n in self.graph.get_all_v():  # to fill up the priority queue
            if n != node:
                heapq.heappush(pq, (float('inf'), n))
            else:
                heapq.heappush(pq, (0, n))
        while len(pq) != 0:  # go until the priority queue is not empty
            heapq.heapify(pq)
            curr_w, curr_n = heapq.heappop(pq)  # take out the smallest distance from the priority queue
            if len(pq) == 0:  # if the pq is now empty
                return curr_w  # this node has the highest weight from the given node and there is the eccentricity
            if curr_w == float('inf'):  # if the weight of the node is inf then the graph is not connected
                return float('inf')
            if curr_w > minWeight:  # if the weight of the node is higher than the given minWeight then this is definitely not the smallest ecc so return -1 flag
                return -1
            for v, w in self.graph.all_out_edges_of_node(curr_n).items():  # go through all of the out edges of the curr_n
                if dijkstra[v] > dijkstra[curr_n] + w:  # if the path through curr_n has a smaller weight then its current weight then relax
                    pq.remove((dijkstra[v], v))
                    dijkstra[v] = dijkstra[curr_n] + w  # relaxing
                    heapq.heappush(pq, (dijkstra[v], v))
        return float('inf')

    def time_to_complete_calls(self, agent: Agent) -> (float, int):
        """
        this function calculates how long it will take for the given agent to catch all of the pokemon its currently after
        :param agent: an agent
        :return: how long it will take for the given agent to catch all of the pokemon its currently after
        """
        time = 0
        position = agent.getSrc() if agent.getDest() != -1 else agent.getDest()
        for src, dest in agent.getFuture_calls():
            ret_time, ret_path = self.shortest_path(position, src)
            time += ret_time / agent.getSpeed()
            position = src
            if dest != -1:
                time += self.getGraph().get_all_e()[(src, dest)] / agent.getSpeed()
                position = dest
        return time, position

    def time_to_complete_calls_with_new_pokemon(self, agent: Agent, pokemon: Pokemon) -> (float, list):
        """
        this function calculates how long it will take to complete the given agent to catch the given pokemon
        :param agent: an agent
        :param pokemon: a new pokemon that appeared in the game
        :return: tuple of the time it takes to catch this pokemon, and the path it takes to do it
        """
        time, position = self.time_to_complete_calls(agent)
        ret_time, ret_path = self.shortest_path(position, pokemon.getOnEdge().getSrc())
        return time+ret_time, ret_path

    def fastest_agent(self, pokemon: Pokemon) -> (int, list, float):
        """
        this function checks which agent can catch this pokemon in the shortest time
        :param pokemon: a new pokemon that appeared in the game
        :return: tuple of the id of the agent, the path it will take to get there, and the amount of time it will take to catch him
        """
        min_time = float('inf')
        ans = -1
        path = []
        for agent in self.agents.values():
            ret_time, ret_path = self.time_to_complete_calls_with_new_pokemon(agent, pokemon)
            if ret_time < min_time:
                min_time = ret_time
                ans = agent.getID()
                path = ret_path
        return ans, path, min_time

    def allocate_agent(self, pokemon: Pokemon, ttl: float) -> None:
        """
        this function allocates the pokemon to an agent
        :param pokemon: a new pokemon that appeared in the game
        :param ttl: time left of the game
        """
        ans, path, time = self.fastest_agent(pokemon)
        self.agents[ans].add_pokemon(pokemon, path, time, ttl, self.graph.get_node(pokemon.getOnEdge().getSrc), self.graph.get_node(pokemon.getOnEdge().getDest))

    def call_move(self, ttl) -> bool:
        """
        this function checks if we need to make any moves
        :param ttl: time left of the game
        :return: return true if a move needs to be called
        """
        flag = False
        for agent in self.agents.values():
            if abs(agent.getFuture_moves()[0] - ttl) < EPSILON:
                agent.getFuture_moves().pop(0)
                flag = True
        return flag

    def choosing_next_edge(self) -> List[tuple]:
        """
        this function finds out which agents need to chose their next edge and returns a list of their choices
        :return: list of agents that needed to choose their next edge with their choices
        """
        choices = []
        for agent in self.agents.values():
            if agent.getDest() == -1:
                next_call = agent.getFuture_calls()[0]
                if next_call[0] != -1:
                    choices.append((agent.getID(), next_call[0]))
                    next_call[0] = -1
                    if next_call[1] == -1:
                        agent.getFuture_calls().pop(0)
                else:
                    choices.append((agent.getID(), next_call[1]))
                    agent.getFuture_calls().pop(0)
        return choices

