import unittest

from math import sqrt

from battle.maptools.direction import Direction, CompositeDirection

N, W, S, E = Direction.N, Direction.W, Direction.S, Direction.E


class TestDirection(unittest.TestCase):

    def test_is_assertion(self):
        self.assertIs(N, Direction.N)
        self.assertIs(S, Direction.S)
        self.assertIs(W, Direction.W)
        self.assertIs(E, Direction.E)

    def test_not_is_assertion(self):
        self.assertIsNot(N, S)

    def test_equality_FAILS(self):
        self.assertTrue(N.__eq__(N))
        self.assertIs(NotImplemented, N.__eq__(S))

        self.assertTrue(N == N)
        self.assertFalse(N == S)
        self.assertTrue(N != S)
        self.assertFalse(N != N)

    def test_enum_not_equal_value_or_name(self):
        self.assertNotEqual(N, 'N')
        self.assertNotEqual('N', N)
        self.assertNotEqual(N, (0, 1))
        self.assertNotEqual((0, 1), N)

    def test_opposite(self):
        self.assertIs(N.opposite(), S)
        self.assertIs(S.opposite(), N)
        self.assertIs(E.opposite(), W)
        self.assertIs(W.opposite(), E)

    def test_left(self):
        self.assertIs(N.left(), W)
        self.assertIs(W.left(), S)
        self.assertIs(S.left(), E)
        self.assertIs(E.left(), N)

    def test_right(self):
        self.assertIs(N.right(), E)
        self.assertIs(E.right(), S)
        self.assertIs(S.right(), W)
        self.assertIs(W.right(), N)

    def test_repr(self):
        self.assertEqual(repr(N), 'Direction.N')
        self.assertEqual(repr(S), 'Direction.S')
        self.assertEqual(repr(E), 'Direction.E')
        self.assertEqual(repr(W), 'Direction.W')

    def test_value_N(self):
        self.assertEqual(N.value, (0, 1))

    def test_value_S(self):
        self.assertEqual(S.value, (0, -1))

    def test_value_E(self):
        self.assertEqual(E.value, (1, 0))

    def test_value_W(self):
        self.assertEqual(W.value, (-1, 0))

    def test_iterator(self):
        order = [N, S, E, W]
        index = 0
        for direction in Direction:
            self.assertIs(order[index], direction)
            index += 1

    def test_lt(self):
        self.assertTrue(S < N)
        self.assertTrue(W < N)
        self.assertTrue(E < N)
        self.assertTrue(S < E)
        self.assertTrue(W < E)
        self.assertTrue(S < W)

        self.assertFalse(N < W)
        self.assertFalse(N < S)
        self.assertFalse(N < E)
        self.assertFalse(E < W)
        self.assertFalse(E < S)
        self.assertFalse(W < S)

        self.assertFalse(N < N)
        self.assertFalse(S < S)
        self.assertFalse(W < W)
        self.assertFalse(E < E)

    def test_le(self):
        self.assertTrue(S <= N)
        self.assertTrue(W <= N)
        self.assertTrue(E <= N)
        self.assertTrue(S <= E)
        self.assertTrue(W <= E)
        self.assertTrue(S <= W)

        self.assertFalse(N <= W)
        self.assertFalse(N <= S)
        self.assertFalse(N <= E)
        self.assertFalse(E <= W)
        self.assertFalse(E <= S)
        self.assertFalse(W <= S)

        self.assertTrue(N <= N)
        self.assertTrue(S <= S)
        self.assertTrue(W <= W)
        self.assertTrue(E <= E)

    def test_gt(self):
        self.assertTrue(N > S)
        self.assertTrue(N > W)
        self.assertTrue(N > E)
        self.assertTrue(E > S)
        self.assertTrue(E > W)
        self.assertTrue(W > S)

        self.assertFalse(W > N)
        self.assertFalse(S > N)
        self.assertFalse(E > N)
        self.assertFalse(W > E)
        self.assertFalse(S > E)
        self.assertFalse(S > W)

        self.assertFalse(N > N)
        self.assertFalse(S > S)
        self.assertFalse(W > W)
        self.assertFalse(E > E)

    def test_ge(self):
        self.assertTrue(N >= S)
        self.assertTrue(N >= W)
        self.assertTrue(N >= E)
        self.assertTrue(E >= S)
        self.assertTrue(E >= W)
        self.assertTrue(W >= S)

        self.assertFalse(W >= N)
        self.assertFalse(S >= N)
        self.assertFalse(E >= N)
        self.assertFalse(W >= E)
        self.assertFalse(S >= E)
        self.assertFalse(S >= W)

        self.assertTrue(N >= N)
        self.assertTrue(S >= S)
        self.assertTrue(W >= W)
        self.assertTrue(E >= E)

    def test_CompositeDirection_string(self):
        test = CompositeDirection(N, N, W, S, E)
        self.assertEqual(str(test), 'NNWSE')

    def test_CompositeDirection_name(self):
        test = CompositeDirection(N, N, W, S, E)
        self.assertEqual(test.name, 'NNWSE')

    def test_CompositeDirection_repr(self):
        test = CompositeDirection(N, N, W)
        self.assertEqual(repr(test), 'CompositeDirection(Direction.N, Direction.N, Direction.W)')

    def test_CompositeDirection_value_one_element(self):
        for direction in Direction:
            float_vals = tuple(float(val) for val in direction.value)
            self.assertEqual(float_vals, CompositeDirection(direction).value)

    def test_CompositeDirection_value_two_elements(self):
        rt_two_over_two = sqrt(2)/2

        self.assertAlmostEqual(CompositeDirection(N, E).value[0], rt_two_over_two, places=7)
        self.assertAlmostEqual(CompositeDirection(N, E).value[1], rt_two_over_two, places=7)

        self.assertAlmostEqual(CompositeDirection(N, W).value[0], -rt_two_over_two, places=7)
        self.assertAlmostEqual(CompositeDirection(N, W).value[1], rt_two_over_two, places=7)

        self.assertAlmostEqual(CompositeDirection(S, E).value[0], rt_two_over_two, places=7)
        self.assertAlmostEqual(CompositeDirection(S, E).value[1], -rt_two_over_two, places=7)

        self.assertAlmostEqual(CompositeDirection(S, W).value[0], -rt_two_over_two, places=7)
        self.assertAlmostEqual(CompositeDirection(S, W).value[1], -rt_two_over_two, places=7)

    def test_CompositeDirection_more_values(self):

        self.assertAlmostEqual(CompositeDirection(N, N, W).value[0], -1/sqrt(5), places=7)
        self.assertAlmostEqual(CompositeDirection(N, N, W).value[1], 2/sqrt(5), places=7)

        self.assertAlmostEqual(CompositeDirection(S, S, S, E).value[0], 1/sqrt(10), places=7)
        self.assertAlmostEqual(CompositeDirection(S, S, S, E).value[1], -3/sqrt(10), places=7)

    def test_CompositeDirection_eq_ne(self):
        self.assertEqual(CompositeDirection(N, N, W), CompositeDirection(W, N, N))

        self.assertNotEqual(CompositeDirection(N, N, W), CompositeDirection(N, N, N, W))

        self.assertNotEqual(CompositeDirection(N), N)

    def test_CompositeDirection_hash(self):
        self.assertEqual(hash(CompositeDirection(N, W)), hash(CompositeDirection(W, N)))

        test = CompositeDirection(N, N, W, N)
        self.assertEqual(hash(test), hash(test.value))

    def test_CompositeDirection_opposite(self):
        test = CompositeDirection(N, N, E)
        self.assertEqual(test.opposite(), CompositeDirection(S, S, W))

    def test_CompositeDirection_left(self):
        test = CompositeDirection(N, N, E)
        self.assertEqual(test.left(), CompositeDirection(W, W, N))
        self.assertEqual(test.left(), CompositeDirection(N, W, W))

    def test_CompositeDirection_right(self):
        test = CompositeDirection(N, N, E)
        self.assertEqual(test.right(), CompositeDirection(E, E, S))

    def test_CompositeDirection_opposite_directions(self):
        self.assertEqual(CompositeDirection(N, N, S), CompositeDirection(N, N, N))

    def test_CompositeDirection_empty_value_raises_value_error(self):
        self.assertRaises(ValueError, CompositeDirection, N, S)
        self.assertRaises(ValueError, CompositeDirection, E, W)
        self.assertRaises(ValueError, CompositeDirection, N, S, E, W)
        self.assertRaises(ValueError, CompositeDirection, N, N, S, S, E, W)

    def test_CompositeDirection_is_unit_vector(self):

        test = CompositeDirection(N, N, W)
        self.assertAlmostEqual(sum(val**2 for val in test.value), 1.0, places=7)

        test = CompositeDirection(S, S, E, S)
        self.assertAlmostEqual(sum(val**2 for val in test.value), 1.0, places=7)

        test = CompositeDirection(W, W, N)
        self.assertAlmostEqual(sum(val**2 for val in test.value), 1.0, places=7)

        test = CompositeDirection(S, S, W, W, W)
        self.assertAlmostEqual(sum(val**2 for val in test.value), 1.0, places=7)
