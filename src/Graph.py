from Edge import Edge
from Node import Node


def build_graph(json: dict) -> (dict, dict):
    """
    this function deserialized a json object (dictionary) and creates a list a nodes and edges that represent a graph
    :param json: a json object (dictionary) that has nodes and edges in it
    :return: a tuple of two dictionaries that represent nodes and edges of a graph
    """
    nodes = {}
    for n in json["Nodes"]:
        x, y, _ = n["pos"].split(",")
        node = Node(int(n["id"]), (float(x), float(y)))
        nodes[node.getID()] = node
    edges = {}
    for e in json["Edges"]:
        edge = Edge(int(e["src"]), int(e["dest"]), float(e["w"]))
        edges[(edge.getSrc(), edge.getDest())] = edge
        nodes[int(e["src"])].add_out_edge(edge)
        nodes[int(e["dest"])].add_in_edge(edge)
    return nodes, edges


class Graph:
    """
    this class represents a graph
    """

    def __init__(self, json: dict):
        self._nodes, self._edges = build_graph(json)

    def v_size(self) -> int:
        """
        returns the amount of nodes in the graph
        """
        return len(self._nodes)

    def e_size(self) -> int:
        """
        returns the amount of edges in the graph
        """
        return len(self._edges)

    def get_node(self, id: int) -> Node:
        return self._nodes[id]

    def get_edge(self, src_dest: tuple) -> Edge:
        return self._edges[src_dest]

    def get_all_v(self) -> dict:
        """
        returns a dictionary of all the nodes in the graph
        """
        return self._nodes

    def get_all_e(self) -> dict:
        """
        returns a dictionary of all the nodes in the graph
        """
        return self._edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        returns a dictionary of all the out edges of a given node
        """
        return self._nodes[id1].getOutEdges()
