import unittest

from battle.actions.target import Target


class TestTarget(unittest.TestCase):
    def test_all_members(self):
        all_members = ~Target.NULL
        self.assertEqual(all_members, (

            Target.ENEMY |
            Target.ALLY |
    
            Target.NEAREST |
            Target.FURTHEST |
    
            Target.STRONGEST |
            Target.WEAKEST |
    
            Target.HIGHEST |
            Target.LOWEST |
    
            Target.HEALTH |
            Target.WEAPON |
            Target.CONCENTRATION |
    
            Target.OPPORTUNITY |
            Target.DANGER |
    
            Target.ADVANTAGE
        ))

    def test_bool(self):
        for target in Target.to_list():
            self.assertTrue(bool(target|Target.ADVANTAGE))
            if target == Target.NULL:
                self.assertFalse(bool(target))
            else:
                self.assertTrue(bool(target))

    def test_null_or(self):
        for target in Target.to_list():
            self.assertEqual(Target.NULL|target, target)

    def test_null_and(self):
        for target in Target.to_list():
            self.assertEqual(Target.NULL&target, Target.NULL)

    def test_has_any_other_is_one_value(self):
        test = Target.ENEMY|Target.DANGER
        self.assertTrue(test.has_any(Target.DANGER))
        self.assertTrue(test.has_any(Target.ENEMY))
        self.assertFalse(test.has_any(Target.ADVANTAGE))

    def test_has_any_other_is_two_value(self):
        test = Target.ENEMY|Target.DANGER
        self.assertTrue(test.has_any(Target.DANGER|Target.ENEMY))
        self.assertTrue(test.has_any(Target.ENEMY|Target.ALLY))
        self.assertFalse(test.has_any(Target.ADVANTAGE|Target.ALLY))

    def test_has_only_other_is_one_value(self):
        test = Target.ENEMY
        self.assertTrue(test.has_only(Target.ENEMY))

        self.assertFalse(test.has_only(Target.DANGER))
        self.assertFalse(test.has_only(Target.ADVANTAGE))

    def test_has_only_other_is_two_value(self):
        test = Target.ENEMY|Target.DANGER
        self.assertTrue(test.has_only(Target.DANGER|Target.ENEMY))

        self.assertFalse(test.has_only(Target.ENEMY|Target.ALLY))
        self.assertFalse(test.has_only(Target.ADVANTAGE|Target.ALLY))

    def test_has_only_test_value_has_more_than_other(self):
        test = Target.ENEMY | Target.DANGER
        self.assertFalse(test.has_only(Target.ENEMY))

    def test_has_at_least_other_is_one_value_true(self):
        other = Target.ENEMY
        self.assertTrue(other.has_at_least(other))
        self.assertTrue((other|Target.ALLY).has_at_least(other))
        self.assertTrue((other|Target.ALLY|Target.DANGER).has_at_least(other))

    def test_has_at_least_other_is_one_value_false(self):
        other = Target.ENEMY
        self.assertFalse(Target.ADVANTAGE.has_at_least(other))
        self.assertFalse((Target.ADVANTAGE | Target.ALLY).has_at_least(other))
        self.assertFalse((Target.ADVANTAGE | Target.ALLY | Target.DANGER).has_at_least(other))

    def test_has_at_least_other_is_two_value_true(self):
        other = Target.ENEMY|Target.HEALTH
        self.assertTrue(other.has_at_least(other))
        self.assertTrue((other|Target.ALLY).has_at_least(other))
        self.assertTrue((other|Target.ALLY|Target.DANGER).has_at_least(other))

    def test_has_at_least_other_is_two_value_false(self):
        other = Target.ENEMY|Target.HEALTH
        self.assertFalse(Target.HEALTH.has_at_least(other))
        self.assertFalse((Target.HEALTH | Target.ALLY).has_at_least(other))
        self.assertFalse((Target.HEALTH | Target.ALLY | Target.DANGER).has_at_least(other))
        self.assertFalse((Target.LOWEST | Target.ALLY | Target.DANGER).has_at_least(other))

    def test_to_list(self):
        answer = [
            Target.ADVANTAGE,
            Target.ALLY,
            Target.CONCENTRATION,
            Target.DANGER,
            Target.ENEMY,
            Target.FURTHEST,
            Target.HEALTH,
            Target.HIGHEST,
            Target.LOWEST,
            Target.NEAREST,
            Target.NULL,
            Target.OPPORTUNITY,
            Target.STRONGEST,
            Target.WEAKEST,
            Target.WEAPON
        ]
        self.assertEqual(answer, Target.to_list())
        