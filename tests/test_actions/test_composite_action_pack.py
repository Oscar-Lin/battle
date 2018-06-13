import unittest

from battle.actions.composite_action import CompositeAction, Action, Target
from battle.actions.composite_action_pack import CompositeActionPack
from battle.players.unit_view import UnitView
from battle.players.units import Soldier, Weapon


class TestCompositeActionPack(unittest.TestCase):

    def setUp(self):
        self.primary = CompositeAction(Action.ATTACK, Target.NULL, 3)
        self.secondary = CompositeAction(Action.MOVE, Target.ENEMY, 2)
        self.tertiary = CompositeAction(Action.ATTACK, Target.ALLY, 1)

        self.pack = CompositeActionPack(self.primary, self.secondary, self.tertiary)

    def test_init(self):
        self.assertEqual(self.pack.primary, self.primary)
        self.assertEqual(self.pack.secondary, self.secondary)
        self.assertEqual(self.pack.tertiary, self.tertiary)

    def test_did_previous_action_fail_false_by_no_previous_action(self):
        self.assertFalse(self.pack.did_previous_action_fail())

    def test_did_previous_action_fail_false_by_change_in_current_action_points(self):
        self.pack.get_next_action(3)
        self.pack.get_next_action(4)
        self.assertFalse(self.pack.did_previous_action_fail())

        self.pack.get_next_action(3)
        self.assertFalse(self.pack.did_previous_action_fail())

    def test_did_previous_action_fail_true_by_no_change_in_current_action_points(self):
        self.pack.get_next_action(3)
        self.pack.get_next_action(3)
        self.assertTrue(self.pack.did_previous_action_fail())

    def test_did_previous_action_fail_does_not_change_current_action_points(self):
        self.pack.get_next_action(3)
        self.pack.get_next_action(3)
        self.assertTrue(self.pack.did_previous_action_fail())
        self.assertTrue(self.pack.did_previous_action_fail())  # if it changed action points, this should be True.

    def test_get_next_action_previous_did_not_fail_no_tertiary_enough_points_for_primary(self):
        self.assertEqual(self.pack.get_next_action(4), self.primary)
        self.assertEqual(self.pack.get_next_action(3), self.primary)

    def test_get_next_action_previous_did_not_fail_no_tertiary_not_enough_points_for_primary_enough_for_secondary(self):
        self.assertEqual(self.pack.get_next_action(3), self.primary)
        self.assertEqual(self.pack.get_next_action(2), self.secondary)

    def test_get_next_action_previous_did_not_fail_only_enough_for_tertiary(self):
        self.assertEqual(self.pack.get_next_action(1), self.tertiary)

    def test_get_next_action_previous_did_not_fail_not_enough_for_any(self):
        self.assertEqual(self.pack.get_next_action(0), CompositeAction.null_action())

    def test_get_next_action_previous_did_not_fail_if_last_was_secondary_can_still_get_primary(self):
        self.assertEqual(self.pack.get_next_action(2), self.secondary)
        self.assertEqual(self.pack.get_next_action(3), self.primary)

    def test_get_next_action_previous_did_not_fail_if_last_was_tertiary_cannot_get_primary_or_secondary(self):
        self.assertEqual(self.pack.get_next_action(1), self.tertiary)
        self.assertEqual(self.pack.get_next_action(3), self.tertiary)
        self.assertEqual(self.pack.get_next_action(2), self.tertiary)

    def test_get_next_action_if_previous_was_null_action_always_null_action(self):
        null = CompositeAction.null_action()
        self.assertEqual(self.pack.get_next_action(0), null)
        self.assertEqual(self.pack.get_next_action(3), null)
        self.assertEqual(self.pack.get_next_action(2), null)
        self.assertEqual(self.pack.get_next_action(1), null)

    def test_get_next_action_previous_failed_previous_was_primary_enough_for_secondary(self):
        self.pack.get_next_action(10)
        self.assertFalse(self.pack.did_previous_action_fail())

        self.assertEqual(self.pack.get_next_action(10), self.pack.secondary)
        self.assertTrue(self.pack.did_previous_action_fail())

    def test_get_next_action_previous_failed_previous_was_primary_not_enough_for_secondary(self):
        primary = CompositeAction(Action.ATTACK, Target.NULL, 3)
        secondary = CompositeAction(Action.MOVE, Target.ENEMY, 4)
        tertiary = CompositeAction(Action.ATTACK, Target.ALLY, 1)

        pack = CompositeActionPack(primary, secondary, tertiary)

        self.assertEqual(pack.get_next_action(3), pack.primary)
        self.assertFalse(pack.did_previous_action_fail())

        self.assertEqual(pack.get_next_action(3), pack.tertiary)
        self.assertTrue(pack.did_previous_action_fail())

    def test_get_next_action_previous_failed_previous_was_primary_not_enough_for_secondary_or_tertiary(self):
        primary = CompositeAction(Action.ATTACK, Target.NULL, 3)
        secondary = CompositeAction(Action.MOVE, Target.ENEMY, 4)
        tertiary = CompositeAction(Action.ATTACK, Target.ALLY, 4)

        pack = CompositeActionPack(primary, secondary, tertiary)

        self.assertEqual(pack.get_next_action(3), pack.primary)
        self.assertFalse(pack.did_previous_action_fail())

        self.assertEqual(pack.get_next_action(3), CompositeAction.null_action())
        self.assertTrue(pack.did_previous_action_fail())

    def test_get_next_action_secondary_failed_goes_to_tertiary_if_able(self):
        self.assertEqual(self.pack.get_next_action(10), self.primary)
        self.assertEqual(self.pack.get_next_action(10), self.secondary)

        self.assertEqual(self.pack.get_next_action(10), self.tertiary)
        self.assertTrue(self.pack.did_previous_action_fail())

    def test_get_next_action_secondary_failed_goes_to_null_if_cannot_tertiary(self):
        new_tertiary = CompositeAction(Action.ATTACK, Target.ADVANTAGE, 100)
        self.pack.tertiary = new_tertiary

        self.assertEqual(self.pack.get_next_action(10), self.primary)
        self.assertEqual(self.pack.get_next_action(10), self.secondary)

        self.assertEqual(self.pack.get_next_action(10), CompositeAction.null_action())
        self.assertTrue(self.pack.did_previous_action_fail())

    def test_get_next_action_tertiary_failed_goes_to_null_action(self):
        self.assertEqual(self.pack.get_next_action(10), self.primary)
        self.assertEqual(self.pack.get_next_action(10), self.secondary)
        self.assertEqual(self.pack.get_next_action(10), self.tertiary)

        self.assertEqual(self.pack.get_next_action(10), CompositeAction.null_action())
        self.assertTrue(self.pack.did_previous_action_fail())

    def test_get_next_action_primary_failed_secondary_success_can_return_to_primary(self):
        self.pack.get_next_action(10)
        self.assertFalse(self.pack.did_previous_action_fail())

        self.assertEqual(self.pack.get_next_action(10), self.pack.secondary)
        self.assertTrue(self.pack.did_previous_action_fail())

        self.assertEqual(self.pack.get_next_action(3), self.pack.primary)
        self.assertFalse(self.pack.did_previous_action_fail())



