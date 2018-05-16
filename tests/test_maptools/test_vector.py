import unittest

from math import sqrt

from battle.maptools.vector import Vector, DangerOpportunity
from battle.maptools.direction import Direction, CompositeDirection

N, S, E, W = Direction


class TestVector(unittest.TestCase):
    def test_init(self):
        v = Vector(2, 5)
        self. assertEqual(v.x, 2)
        self.assertEqual(v.y, 5)

        v = Vector(0, 0)
        self. assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)

        v = Vector(-2, -5)
        self. assertEqual(v.x, -2)
        self.assertEqual(v.y, -5)

    def test_from_dir_and_mag(self):
        v = Vector.from_dir_and_mag(N, 10)
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 10)

        v = Vector.from_dir_and_mag(S, 10)
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, -10)

        v = Vector.from_dir_and_mag(E, 10)
        self.assertEqual(v.x, 10)
        self.assertEqual(v.y, 0)

        v = Vector.from_dir_and_mag(W, 10)
        self.assertEqual(v.x, -10)
        self.assertEqual(v.y, 0)

    def test_from_dir_and_mag_composite_direction(self):
        v = Vector.from_dir_and_mag(CompositeDirection(N, E), 5)
        expected_x_y = 5 / sqrt(2)
        self.assertAlmostEqual(v.x, expected_x_y, places=7)
        self.assertAlmostEqual(v.y, expected_x_y, places=7)

    def test_add(self):
        v1 = Vector(3, 6)
        v2 = Vector(-1, 2)
        v3 = v1.add(v2)
        self.assertEqual(v3.x, 2)
        self.assertEqual(v3.y, 8)

    def test_direction_tuple_positive(self):
        v = Vector(2, 3)
        self.assertEqual(v.direction_tuple(), ((E, 2), (N, 3)))

    def test_direction_tuple_zero(self):
        v = Vector(0, 0)
        self.assertEqual(v.direction_tuple(), ((E, 0), (N, 0)))

    def test_direction_tuple_negative(self):
        v = Vector(-2, -3)
        self.assertEqual(v.direction_tuple(), ((W, 2), (S, 3)))

    def test_eq_true(self):
        self.assertTrue(Vector(1, 2).__eq__(Vector(1, 2)))

    def test_eq_false(self):
        self.assertFalse(Vector(2, 2).__eq__(Vector(1, 2)))
        self.assertFalse(Vector(1, 1).__eq__(Vector(1, 2)))

    def test_ne_false(self):
        self.assertFalse(Vector(1, 2).__ne__(Vector(1, 2)))

    def test_ne_true(self):
        self.assertTrue(Vector(2, 2).__ne__(Vector(1, 2)))
        self.assertTrue(Vector(1, 1).__ne__(Vector(1, 2)))

    def test_repr(self):
        self.assertEqual(repr(Vector(1, -1)), 'Vector(1, -1)')

    def test_dangeroppurtunity_init(self):
        vector_a = Vector(1, 2)
        vector_b = Vector(3, 4)
        test = DangerOpportunity(vector_a, vector_b)
        self.assertEqual(test.danger, vector_a)
        self.assertEqual(test.opportunity, vector_b)

    def test_dangeroppurtunity_empty(self):
        test = DangerOpportunity.empty()
        self.assertEqual(test.danger, Vector(0, 0))
        self.assertEqual(test.opportunity, Vector(0, 0))

    def test_dangeroppurtunity_eq_true(self):
        vector_a = Vector(1, 2)
        vector_b = Vector(3, 4)
        self.assertEqual(DangerOpportunity(vector_a, vector_b), DangerOpportunity(vector_a, vector_b))

    def test_dangeroppurtunity_eq_false_by_type(self):
        vector_a = Vector(1, 2)
        vector_b = Vector(3, 4)
        self.assertNotEqual(DangerOpportunity(vector_a, vector_b), (vector_a, vector_b))

    def test_dangeroppurtunity_eq_false_by_order(self):
        vector_a = Vector(1, 2)
        vector_b = Vector(3, 4)
        self.assertNotEqual(DangerOpportunity(vector_a, vector_b), DangerOpportunity(vector_b, vector_a))

    def test_dangeroppurtunity_eq_false_by_number(self):
        vector_a = Vector(1, 2)
        vector_b = Vector(3, 4)
        vector_c = Vector(-1, 0)
        self.assertNotEqual(DangerOpportunity(vector_a, vector_b), DangerOpportunity(vector_a, vector_c))

    def test_add_empty(self):
        vector_a = Vector(1, 2)
        vector_b = Vector(3, 4)
        test = DangerOpportunity(vector_a, vector_b)
        new = test.add(DangerOpportunity.empty())
        self.assertEqual(test, new)
        self.assertIsNot(test, new)

    def test_add_non_empty(self):
        vector_a = Vector(1, 2)
        vector_b = Vector(3, 5)
        test = DangerOpportunity(vector_a, vector_b)
        to_add = DangerOpportunity(Vector(1, 1), Vector(-1, -1))
        expected = DangerOpportunity(Vector(2, 3), Vector(2, 4))
        self.assertEqual(test.add(to_add), expected)
