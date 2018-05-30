import random
from typing import List

from battle.maptools.vector import DangerOpportunity
from battle.maptools.footprint import FootPrint, FootPrintPackage, Token
from battle.maptools.map import Map
from battle.players.team import Team
from battle.players.units import Soldier
from battle.perimiterlistener import PerimeterListener
from battle.rangefinder import RangeFinder
from battle.movementcalculator import MovementCalculator
from battle.turn_execution.target_finder import TargetFinder


class Actionator(object):
    def __init__(self, unit: Soldier, action, perimeter_listener: PerimeterListener, map_: Map, teams: List[Team]):
        self._unit = unit
        self._action = action
        self._pl = perimeter_listener
        self._map = map_
        self._mc = MovementCalculator(self._map)
        self._teams = teams[:]

    def _get_targets_in_range(self):
        tf = TargetFinder(self._map, self._teams)
        return tf.enemies_in_range(self._unit)

    def _get_targets_in_sight(self):
        tf = TargetFinder(self._map, self._teams)
        return tf.enemies_in_sight(self._unit)
    
    def go(self):  # TODO do something
        # if self._action.has_any(Action.ATTACK):
        #     self.attack()
        # else:
        #     self.move()
        pass

    def move(self):
        current_pt = self._map.get_point(self._unit)
        mv_pts, path = self.get_path()  # a generator of pts not including current point
        ally = None  # type: Team
        for team in self._teams:
            if team.is_on_team(self._unit):
                ally = team
                break
        end_point = current_pt
        for point in path:
            end_point = point
            attackers = self._pl.get_attackers(point) # type: List[Soldier]
            for attacker in attackers:
                if not ally.is_on_team(attacker) and attacker.can_act(attacker.get_weapon().action_pts):
                    attacker.attack(self._unit)
        self._unit.move(mv_pts)
        self._map.remove_unit(current_pt)
        self._map.place_unit(self._unit, end_point)
        self._pl.rm_perimeter(self._unit)
        self._pl.set_perimeter(self._unit, end_point)

    def attack(self):  # TODO experimental idea
        self._unit.attack(self.get_target())

    def get_target(self):
        pass
        # self._get_targets_in_range()
        # self._get_targets_in_sight()

    def get_path(self):
        max_mv = self._get_max_mv()
        location = self._map.get_point(self._unit)
        raw = self._mc.get_movement_points_with_path(location, max_mv)

        mv_pts, destination_path = max(raw.values()) # TODO

        return mv_pts, location.generate_path(destination_path)

    def _get_max_mv(self):
        return self._unit.get_action_points()


class TurnCoordinator(object):
    def __init__(self, map_: Map, team_1: Team, team_2: Team):
        self._map = map_
        self._team_1 = team_1
        self._team_2 = team_2
        self._pm = PerimeterListener(self._map)
        self._mc = MovementCalculator(self._map)
        self._rf = RangeFinder(self._map)

        self._unmoved_units = []

    def get_ally_enemy(self, unit):
        if self._team_1.is_on_team(unit):
            return self._team_1, self._team_2
        return self._team_2, self._team_1

    def create_turn_order(self):
        team_1_list = self._team_1.deployed
        team_2_list = self._team_2.deployed
        turn_order = team_1_list + team_2_list
        random.shuffle(turn_order)
        self._unmoved_units = turn_order

    def show_turn_order(self):
        return self._unmoved_units[:]

    def get_action_list(self, unit: Soldier):
        point = self._map.get_point(unit)
        ally, enemy = self.get_ally_enemy(unit)
        vectors = self._map.get_tile(point).footprint_vectors()
        ally_vector = vectors.get(ally, DangerOpportunity.empty())
        enemy_vector = vectors.get(enemy, DangerOpportunity.empty())
        return unit.strategy.get_action(ally_vector, enemy_vector)

    def do_actions(self, unit: Soldier):
        action_list = self.get_action_list(unit)
        while unit.get_action_points():
            for action in action_list:
                actionator = Actionator(unit, action, self._pm, self._map, [self._team_1, self._team_2])
                actionator.go()
                
    def one_turn(self):
        self.create_turn_order()
        for unit in self._unmoved_units:
            self.do_actions(unit)
