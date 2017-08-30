import unittest

from battle.maptools.direction import Direction
from battle.maptools.point import Point

N, S, E, W = Direction.N, Direction.S, Direction.E, Direction.W


class TestPoint(unittest.TestCase):
    def test_init(self):
        point = Point(1, 2)
        self.assertEqual(point.x, 1)
        self.assertEqual(point.y, 2)

    def test_eq_true(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        self.assertTrue(p1.__eq__(p2))

    def test_eq_false(self):
        p1 = Point(1, 2)
        p2 = Point(1, 1)
        self.assertFalse(p1.__eq__(p2))
        self.assertFalse(p1.__eq__((1, 2)))

    def test_ne_true(self):
        p1 = Point(1, 2)
        p2 = Point(1, 1)
        self.assertTrue(p1.__ne__(p2))
        self.assertTrue(p1.__ne__((1, 2)))

    def test_ne_false(self):
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        self.assertFalse(p1.__ne__(p2))

    def test_lt_by_y(self):
        p1 = Point(1, 2)
        p2 = Point(10, 1)
        self.assertTrue(p2.__lt__(p1))
        self.assertFalse(p1.__lt__(p2))

    def test_lt_by_x(self):
        p1 = Point(3, 1)
        p2 = Point(2, 1)
        self.assertTrue(p2.__lt__(p1))
        self.assertFalse(p1.__lt__(p2))
        self.assertFalse(p1.__lt__(p1))
        
    def test_le(self):
        p1 = Point(1, 1)
        p2 = Point(0, 0)
        self.assertTrue(p1.__le__(p1))
        self.assertTrue(p2.__le__(p1))
        self.assertFalse(p1.__le__(p2))

    def test_gt(self):
        p1 = Point(2, 1)
        p2 = Point(3, 1)
        self.assertTrue(p2.__gt__(p1))
        self.assertFalse(p1.__gt__(p2))
        self.assertFalse(p1.__gt__(p1))
        
    def test_ge(self):
        p1 = Point(1, 1)
        p2 = Point(2, 2)
        self.assertTrue(p1.__ge__(p1))
        self.assertTrue(p2.__ge__(p1))
        self.assertFalse(p1.__ge__(p2))

    def test_str(self):
        self.assertEqual(str(Point(-1, 2)), '(-1, 2)')

    def test_repr(self):
        self.assertEqual(repr(Point(1, 2)), 'Point(1, 2)')

    def test_hash(self):
        self.assertEqual(hash(Point(1, 2)), hash('Point(1, 2)'))
        
    def test_north(self):
        point = Point(1, 2)
        self.assertEqual(point.in_direction(N), Point(1, 3))

    def test_south(self):
        point = Point(1, 2)
        self.assertEqual(point.in_direction(S), Point(1, 1))

    def test_east(self):
        point = Point(1, 2)
        self.assertEqual(point.in_direction(E), Point(2, 2))

    def test_west(self):
        point = Point(1, 2)
        self.assertEqual(point.in_direction(W), Point(0, 2))

    def test_plus_zero_zero(self):
        self.assertEqual(Point(1, 1).plus(0, 0), Point(1, 1))

    def test_plus_neg_pos(self):
        self.assertEqual(Point(1, 1).plus(-2, 2), Point(-1, 3))

    def test_plus_pos_neg(self):
        self.assertEqual(Point(1, 1).plus(2, -2), Point(3, -1))

    def test_at_distance_zero(self):
        answer = Point(-5, 2).at_distance(0)
        self.assertEqual(answer, [Point(-5, 2)])

    def test_at_distance(self):
        answer = Point(1, 1).at_distance(1)
        expected = [Point(1, 0),
                    Point(0, 1), Point(2, 1),
                    Point(1, 2)]
        self.assertEqual(answer, expected)

    def test_at_distance_second_test(self):
        answer = Point(0, 0).at_distance(2)
        expected = [Point(0, -2),
                    Point(-1, -1), Point(1, -1),
                    Point(-2, 0), Point(2, 0),
                    Point(-1, 1), Point(1, 1),
                    Point(0, 2)]
        self.assertEqual(answer, expected)

    def test_to_rectangle_one_by_one(self):
        self.assertEqual(Point(1, 1).to_rectangle(1, 1), [Point(1, 1)])
        self.assertEqual(Point(1, 1).to_rectangle(-1, 1), [Point(1, 1)])
        self.assertEqual(Point(1, 1).to_rectangle(1, -1), [Point(1, 1)])

    def test_to_rectangle_zero_by_num(self):
        self.assertEqual(Point(1, 1).to_rectangle(0, 5), [])

    def test_to_rectangle_num_by_zero(self):
        self.assertEqual(Point(1, 1).to_rectangle(5, 0), [])

    def test_to_rectangle_pos_pos(self):
        answer = [Point(0, 0), Point(1, 0), Point(2, 0),
                  Point(0, 1), Point(1, 1), Point(2, 1)]
        self.assertEqual(Point(0, 0).to_rectangle(3, 2), answer)

    def test_to_rectangle_neg_neg(self):
        answer = [Point(-2, -1), Point(-1, -1), Point(0, -1),
                  Point(-2, 0), Point(-1, 0), Point(0, 0)]
        self.assertEqual(Point(0, 0).to_rectangle(-3, -2), answer)

    def test_to_rectangle_pos_neg(self):
        answer = [Point(0, -1), Point(1, -1), Point(2, -1),
                  Point(0, 0), Point(1, 0), Point(2, 0)]
        self.assertEqual(Point(0, 0).to_rectangle(3, -2), answer)

    def test_to_rectangle_neg_pos(self):
        answer = [Point(-2, 0), Point(-1, 0), Point(0, 0),
                  Point(-2, 1), Point(-1, 1), Point(0, 1)]
        self.assertEqual(Point(0, 0).to_rectangle(-3, 2), answer)

    def test_follow_path(self):
        raise NotImplementedError

if __name__ == '__main__':
    unittest.main()
