from unittest import TestCase

from src.Point2D import Point2D


class TestPoint2D(TestCase):
    def test_get_x(self):
        point = Point2D((35,32))
        self.assertEqual(point.getX(), 35)

    def test_get_y(self):
        point = Point2D((35,32))
        self.assertEqual(point.getY(), 32)

    def test_get_pos_as_tuple(self):
        point = Point2D((35,32))
        self.assertEqual(point.getPosAsTuple(), (35,32))

    def test_update_pos(self):
        point = Point2D((35,32))
        point.updatePos((22,23))
        self.assertEqual(point.getPosAsTuple(), (22,23))
