from unittest import TestCase

from src.Edge import Edge
from src.Node import Node


class TestNode(TestCase):
    def test_get_id(self):
        node = Node(0, (35, 32))
        self.assertEqual((node.getID()), 0)

    def test_get_pos(self):
        node = Node(0, (35, 32))
        self.assertEqual((node.getPos()), (35,32))

    def test_get_out_edges(self):
        node = Node(0, (35, 32))
        edge = Edge(0,3,8)
        node.add_out_edge(edge)
        self.assertEqual(node.getOutEdges()[3], 8)

    def test_get_in_edges(self):
        node = Node(0, (35, 32))
        edge = Edge(3,0,8)
        node.add_in_edge(edge)
        self.assertEqual(node.getInEdges()[3], 8)

    def test_get_weight(self):
        node = Node(0, (35, 32))
        self.assertEqual((node.getWeight()), 0)

    def test_set_weight(self):
        node = Node(0, (35, 32))
        node.set_weight(2.5)
        self.assertEqual((node.getWeight()), 2.5)

    def test_add_in_edge(self):
        node = Node(0, (35, 32))
        edge = Edge(3,0,8)
        node.add_in_edge(edge)
        self.assertEqual(node.getInEdges()[3], 8)

    def test_add_out_edge(self):
        node = Node(0, (35, 32))
        edge = Edge(0,3,8)
        node.add_out_edge(edge)
        self.assertEqual(node.getOutEdges()[3], 8)
