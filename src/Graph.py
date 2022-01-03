"""
represents a graph
"""
from src.Edge import Edge
from src.Node import Node


def build_graph(json: dict) -> (dict, dict):
    nodes = {}
    for n in json["Nodes"]:
        x, y, _ = n["pos"].split(",")
        node = Node(int(n["id"]), (float(x), float(y)))
        nodes[node.getID()] = node
    edges = {}
    for e in json["Edges"]:
        edge = Edge(int(e["src"]), int(e["dest"]), float(e["w"]))
        edges[(edge.getSrc(), edge.getDest())] = edge
    return nodes, edges


class Graph:

    def __init__(self, json: dict):
        self.nodes, self.edges = build_graph(json)
