"""
class that holds all of the functions that will be used for graphs
"""
import math

from src import Pokemon, Point2D
from src.Graph import Graph

EPSILON = 0.001


def find_edge_with_pokemon(type: int, pos: Point2D, graph: Graph):
    for e in graph.edges:
        if type > 0 and e.getSrc() < e.getDest():
            if math.dist(graph.nodes.get(e.getSrc()).getPos(), pos) + math.dist(pos, graph.nodes.get(e.getDest()).getPos()) < math.dist(graph.nodes.get(e.getSrc()).getPos(), graph.nodes.get(e.getDest()).getPos()) + EPSILON:
                return e
    print("POKEMON NOT ON GRAPH!")


class GraphAlgos:

    def __init__(self, json: dict):
        self.graph = Graph(json)

    def getGraph(self):
        return self.graph
