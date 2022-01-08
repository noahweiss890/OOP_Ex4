from unittest import TestCase

from src.Edge import Edge


class TestEdge(TestCase):
    def test_get_src(self):
        edge = Edge(1,3,8)
        self.assertEqual(edge.getSrc(), 1)

    def test_get_dest(self):
        edge = Edge(1,3,8)
        self.assertEqual(edge.getDest(), 3)

    def test_get_weight(self):
        edge = Edge(1,3,8)
        self.assertEqual(edge.getWeight(), 8)
