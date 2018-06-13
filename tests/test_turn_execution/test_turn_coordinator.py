import unittest
import random

from battle.turn_execution.turn_coordinator import TurnCoordinator, Actionator
from battle.maptools.tile import Tile
from battle.maptools.point import Point
from battle.maptools.map import Map
from battle.players.team import Team
from battle.players.units import Soldier
from battle.perimiterlistener import PerimeterListener
from battle.maptools.footprint import FootPrintPackage, FootPrint, Token
from battle.maptools.vector import Vector
from battle.maptools.direction import Direction


N, S, E, W = Direction


class TestTurnCoordinator(unittest.TestCase):
    def setUp(self):
        self.map_length = 20
        self.map = Map(self.map_length, self.map_length, [Tile() for _ in range(self.map_length**2)])
        self.team_a = Team(Point(self.map_length-1, 0), self.map)
        self.team_b = Team(Point(0, self.map_length-1), self.map)

        team_size = 3
        self.a_units = [Soldier() for _ in range(team_size)]
        self.b_units = [Soldier() for _ in range(team_size)]

        for a_unit, b_unit in zip(self.a_units, self.b_units):
            self.team_a.add_player(a_unit)
            self.team_b.add_player(b_unit)

        self.tc = TurnCoordinator(self.map, self.team_a, self.team_b)

    def test_get_ally_enemy(self):

        self.assertEqual(self.tc.get_ally_enemy(self.a_units[0]), (self.team_a, self.team_b))
        self.assertEqual(self.tc.get_ally_enemy(self.b_units[0]), (self.team_b, self.team_a))

    def test_create_turn_order(self):
        for _ in range(2):
            self.team_a.spawn()
        for _ in range(2):
            self.team_b.spawn()
        team_a_list = self.team_a.deployed
        team_b_list = self.team_b.deployed
        all_units = team_a_list + team_b_list

        random.seed(8)

        self.tc.create_turn_order()
        turn_order = self.tc.show_turn_order()

        self.assertEqual(set(all_units), set(turn_order))
        self.assertEqual(len(all_units), len(turn_order))
        self.assertNotEqual(all_units, turn_order)

        self.tc.create_turn_order()
        turn_order_2 = self.tc.show_turn_order()

        self.assertEqual(set(all_units), set(turn_order_2))
        self.assertEqual(len(all_units), len(turn_order_2))
        self.assertNotEqual(all_units, turn_order_2)
        self.assertNotEqual(turn_order, turn_order_2)

    def test_get_action_list(self):  # TODO  UNFINISHED TEST
        fpp = FootPrintPackage()
        fp_1 = FootPrint(Token.DANGER, W, self.team_a)
        fp_2 = FootPrint(Token.NEUTRAL, N, self.team_b)
        fpp.push(fp_1)
        fpp.push(fp_2)
        self.map.place_unit(self.a_units[0], Point(1, 1))
        expected = self.tc.get_action_list(self.a_units[0])
        print('test_turn_coordinator', expected)

    def test_do_actions(self):
        pass

    def test_one_turn(self):
        pass


class TestActionator(unittest.TestCase):
    def setUp(self):
        self.map_length = 20
        self.map = Map(self.map_length, self.map_length, [Tile() for _ in range(self.map_length**2)])
        self.unit = Soldier()
        self.pl = PerimeterListener(self.map)
        self.team_a = Team(Point(self.map_length - 1, 0), self.map)
        self.team_b = Team(Point(0, self.map_length - 1), self.map)
        self.team_list = [self.team_a, self.team_b]

        team_size = 3
        self.a_units = [Soldier() for _ in range(team_size)]
        self.b_units = [Soldier() for _ in range(team_size)]

        for a_unit, b_unit in zip(self.a_units, self.b_units):
            self.team_a.add_player(a_unit)
            self.team_b.add_player(b_unit)

    def test_go_attack(self):
        pass

    def test_go_move(self):
        pass

    def test_move(self):
        pass

    def test_get_path(self):
        pass
