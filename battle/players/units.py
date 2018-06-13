from typing import Union

from battle.players.unit_view import UnitView
from battle.players.strategy import WanderAndFight
from battle.statstools.stat import PositiveStat
from battle.weapon import MeleeWeapon, RangedWeapon, Weapon, OutOfAmmo


FIST = MeleeWeapon(dmg=1, action_pts=1)
GUN = RangedWeapon(dmg=5, action_pts=2, range_=5, ammo=10)


class Soldier(object):
    def __init__(self, action_pts: int = 3, health: Union[float, int] = 100, heal_pct: float = 5.0):

        self._action_pts = PositiveStat(action_pts)
        self._health = PositiveStat(health)

        self._healing_pct = heal_pct

        self._weapon = FIST

        self._strategy = WanderAndFight(UnitView(self))

    @property
    def strategy(self):
        return self._strategy

    def get_perimeter_size(self) -> int:
        return self._weapon.range

    def get_sight_range(self) -> int:
        return 10

    def get_action_points(self) -> int:
        return self._action_pts.current

    def can_act(self, action_pts) -> bool:
        return action_pts <= self._action_pts.current and not self.is_dead()

    def move(self, mv_pts):
        if mv_pts < 0:
            raise ValueError('mv_pts can\'t be less than zero')
        if self.can_act(mv_pts):
            self._action_pts.modify_current(-mv_pts)

    def reset_move_points(self):
        self._action_pts.reset()

    def get_health(self) -> int:
        return self._health.current

    def get_weapon(self) -> Weapon:
        return self._weapon

    def equip_weapon(self, weapon: Weapon):
        self._weapon = weapon

    def attack(self, opponent):
        action_pts = self._weapon.action_pts
        if not self.can_act(action_pts):
            return None
        self._action_pts.modify_current(-action_pts)
        try:
            dmg = self._weapon.use_weapon()
            opponent.receive_dmg(dmg)
        except OutOfAmmo:
            self._weapon.refill_ammo()

    def is_dead(self) -> bool:
        return self._health.current <= 0

    def receive_dmg(self, dmg: int):
        if dmg < 0:
            raise ValueError('damage can\'t be less than zero')
        self._health.modify_current(-dmg)

    def heal(self, health_pts: int):
        """cannot heal past max"""
        if health_pts < 0:
            raise ValueError('health_pts can\'t be less than zero')
        if self.is_dead():
            return None
        self._health.modify_current(health_pts)

    def rest(self):
        """heal and reset_move"""
        heal_points = int(round(self._health.max * self._healing_pct / 100.))
        self.heal(heal_points)
        self.reset_move_points()


class Base(Soldier):
    def __init__(self):
        super(Base, self).__init__(action_pts=0, health=float('inf'), heal_pct=0)



