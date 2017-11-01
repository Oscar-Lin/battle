from battle.maptools.map import Map
from battle.maptools.tile import Tile
from battle.maptools.point import Point
from battle.maptools.direction import Direction

from battle.weapon import RangedWeapon, MeleeWeapon, OutOfAmmo
from battle.units import Soldier

from battle.rangefinder import RangeFinder
from battle.movementcalculator import MovementCalculator
from battle.perimiterlistener import PerimeterListener


class Coordinator(object):
    def __init__(self, map_: Map):
        self._map = map_

        self._range_find = RangeFinder(self._map)
        self._move_calc = MovementCalculator(self._map)
        self._listener = PerimeterListener(self._map)

        self._units = self._get_all_units()

    def _get_all_units(self):
        raise NotImplementedError

    def do_a_turn(self):
        for soldier in self._units:
            self.act(soldier)

    def act(self, soldier: Soldier):
        raise NotImplementedError

    def find_enemy(self, solder: Soldier):
        raise NotImplementedError


if __name__ == '__main__':
    the_tiles = []
    the_map = Map("width", "height", the_tiles)
    red_team = [("soldier", "pt")]
    blue_team = []
    for soldier, point in red_team:
        the_map.place_unit(soldier, point)

    for soldier, point in blue_team:
        the_map.place_unit(soldier, point)

    just_do_it = Coordinator(the_map)
    for _ in range(5):
        just_do_it.do_a_turn()
        print('some stuff you want to know')

