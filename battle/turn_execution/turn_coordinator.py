import random

from battle.maptools.vector import DangerOpportunity
from battle.maptools.footprint import FootPrint, FootPrintPackage, Token
from battle.maptools.map import Map
from battle.players.team import Team
from battle.players.units import Soldier
from battle.perimiterlistener import PerimeterListener
from battle.rangefinder import RangeFinder
from battle.movementcalculator import MovementCalculator
from battle.turn_execution.target_finder import TargetFinder
from battle.players.action import Action


class Actionator(object):
    def __init__(self, unit: Soldier, action: Action, perimeter_listener: PerimeterListener, map_: Map, teams: list):
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
    
    def go(self):
        if self._action.has_any(Action.ATTACK):
            self.attack()
        else:
            self.move()

    def move(self):
        self._map.get_point(self._unit)
        path = self.get_path()
        #CompositeDirection
        #target = self.get_target()


        for point in path:
            attacker = self._pl.get_attackers(point)

        """
                        get location
                        get path  list of points
                            sight range, enemy ally
                            attack range, enemy


                        for point in path:
                            check perimeter listener
                            check target, action_limit
                        jump to destination
                        set pl

                        pseudo-code
                        """

    def attack(self):
        pass

    def get_target(self):
        # self._get_targets_in_range()
        # self._get_targets_in_sight()

    def get_path(self):
        max_mv = self._get_max_mv()
        return self._mc.get_movement_points_with_path(self._map.get_point(self._unit), max_mv)

    def _get_max_mv(self):
        return self._unit.get_action_points()


    """
    hw - type out in pseudo-code, how you will decide where someone moves and how far?
    actions:
    NULL

    GO
    STAY
    ATTACK

    ENEMY
    ALLY

    NEAREST
    FURTHEST

    STRONGEST
    WEAKEST

    HIGHEST
    LOWEST

    HEALTH
    WEAPON
    CONCENTRATION

    OPPORTUNITY
    DANGER

    TOWARDS
    AWAY



    """


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
