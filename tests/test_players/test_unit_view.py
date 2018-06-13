import unittest

from battle.players.unit_view import UnitView
from battle.players.units import Soldier, RangedWeapon, FIST

class TestUnitView(unittest.TestCase):
    def test_init(self):
        unit = Soldier()
        unit_view = UnitView(unit)

        self.assertEqual(unit_view.available_action_pts, unit.get_action_points())
        self.assertEqual(unit_view.attack_action_pts, unit.get_weapon().action_pts)
        self.assertEqual(unit_view.health, unit.get_health())
        self.assertEqual(unit_view.perimeter_range, unit.get_perimeter_size())
        self.assertEqual(unit_view.sight_range, unit.get_sight_range())
        self.assertEqual(unit_view.weapon_range, unit.get_weapon().range)
        self.assertEqual(unit_view.uses_melee_weapon, unit.get_weapon().is_melee_weapon())

    def test_unit_changes_view_changes(self):
        unit = Soldier()
        unit_view = UnitView(unit)

        self.assertEqual(unit.get_weapon(), FIST)

        new_weapon = RangedWeapon(100, 100, 100, 100)
        self.assertNotEqual(FIST.action_pts, new_weapon.action_pts)
        self.assertNotEqual(FIST.range, new_weapon.range)
        self.assertNotEqual(FIST.dmg, new_weapon.dmg)
        self.assertNotEqual(FIST.ammo, new_weapon.ammo)
        self.assertNotEqual(FIST.is_melee_weapon(), new_weapon.is_melee_weapon())

        self.assertEqual(unit.get_health(), 100)
        self.assertEqual(unit.get_action_points(), 3)

        unit.equip_weapon(new_weapon)
        unit.move(2)
        unit.receive_dmg(2)

        self.assertEqual(unit_view.available_action_pts, 1)
        self.assertEqual(unit_view.attack_action_pts, 100)
        self.assertEqual(unit_view.health, 98)
        self.assertEqual(unit_view.perimeter_range, unit.get_perimeter_size())
        self.assertEqual(unit_view.sight_range, unit.get_sight_range())
        self.assertEqual(unit_view.weapon_range, 100)
        self.assertEqual(unit_view.uses_melee_weapon, False)

    def test_unit_view_cannot_assign_values(self):
        unit = Soldier()
        unit_view = UnitView(unit)

        all_keys = [key for key in unit_view.__dir__() if not key.startswith('_')]

        for key in all_keys:
            self.assertRaises(AttributeError, setattr, unit_view, key, 5)