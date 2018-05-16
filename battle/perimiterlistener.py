from battle.maptools.map import Map
from battle.maptools.point import Point
from battle.players.units import Soldier
from battle.rangefinder import RangeFinder
from battle.weapon import RangedWeapon


class PerimeterListener(object):
    def __init__(self, map_: Map) -> None:
        self._map = map_
        self._range_finder = RangeFinder(self._map)
        map_pts = Point(0, 0).to_rectangle(*self._map.get_size())
        self._watchers_at_point = {pt: set() for pt in map_pts}

    def set_perimeter(self, unit: Soldier, point: Point):
        range_dict = self._get_range_dict(unit, point)
        del range_dict[0]
        for pt_advantage_list in range_dict.values():
            for pair in pt_advantage_list:
                self._watchers_at_point[pair[0]].add(unit)

    def _get_range_dict(self, unit, point):
        max_range = unit.get_perimeter_size()
        if not unit.get_weapon().is_melee_weapon():
            range_dict = self._range_finder.get_attack_ranges_ranged(point, max_range)
        else:
            range_dict = self._range_finder.get_attack_ranges_melee(point, max_range)
        return range_dict

    def rm_perimeter(self, unit: Soldier):
        for units in self._watchers_at_point.values():
            units.discard(unit)

    def get_attackers(self, point: Point) -> set:
        return self._watchers_at_point[point].copy()
