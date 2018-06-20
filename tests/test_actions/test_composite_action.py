import unittest

from battle.actions.composite_action import CompositeAction, Target, Action


class TestCompositeAction(unittest.TestCase):
    def test_init(self):
        action = CompositeAction(Action.ATTACK, Target.ENEMY, 1)
        self.assertEqual(action.action, Action.ATTACK)
        self.assertEqual(action.target, Target.ENEMY)
        self.assertEqual(action.floor, 1)

    def test_eq_false_by_type(self):
        action = CompositeAction(Action.ATTACK, Target.ENEMY, 1)
        args = (Action.ATTACK, Target.ENEMY, 1)
        self.assertFalse(action.__eq__(args))

    def test_eq_false_by_values(self):
        action = CompositeAction(Action.ATTACK, Target.ENEMY, 1)
        by_action = CompositeAction(Action.MOVE, Target.ENEMY, 1)
        by_target = CompositeAction(Action.ATTACK, Target.NULL, 1)
        by_floor = CompositeAction(Action.ATTACK, Target.ENEMY, 2)

        self.assertFalse(action.__eq__(by_action))
        self.assertFalse(action.__eq__(by_target))
        self.assertFalse(action.__eq__(by_floor))

    def test_eq_true(self):
        action = CompositeAction(Action.ATTACK, Target.ENEMY, 1)
        other = CompositeAction(Action.ATTACK, Target.ENEMY, 1)
        self.assertTrue(action.__eq__(other))
        self.assertEqual(action, other)

    def test_repr(self):
        action = CompositeAction(Action.ATTACK, Target.ENEMY, 1)
        self.assertEqual(repr(action), 'CompositeAction(<Action.ATTACK: 1>, <Target.ENEMY: 1>, 1)')

    def test_hash(self):
        action = CompositeAction(Action.ATTACK, Target.ENEMY, 1)
        self.assertEqual(hash(action), hash('CompositeAction(<Action.ATTACK: 1>, <Target.ENEMY: 1>, 1)'))

    def test_null_action(self):
        self.assertEqual(CompositeAction.null_action(), CompositeAction(Action.NULL, Target.NULL, 0))

    def test_bool_true(self):
        for action in Action:
            for target in Target:
                self.assertTrue(CompositeAction(action, target, 1))
                if action != Action.NULL or target != Target.NULL:
                    self.assertTrue(CompositeAction(action, target, 0))

    def test_bool_false(self):
        self.assertFalse(CompositeAction.null_action())

