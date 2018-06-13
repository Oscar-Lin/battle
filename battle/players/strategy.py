import random
from typing import List, Tuple

from battle.maptools.footprint import DangerOpportunity
from battle.actions.composite_action_pack import CompositeActionPack
from battle.actions.composite_action import CompositeAction
from battle.actions.target import Target
from battle.actions.action import Action
from battle.maptools.vector import Vector
from battle.players.unit_view import UnitView


class Strategy(object):
    multipliers = {
        ('ally', 'danger'): 1,
        ('ally', 'opportunity'): 1,
        ('enemy', 'danger'): 1,
        ('enemy', 'opportunity'): 1
    }

    def __init__(self, unit_view: UnitView):
        self.unit_view = unit_view

    @classmethod
    def prioritize_vectors(cls, ally: DangerOpportunity, enemy: DangerOpportunity) -> List[Tuple[str]]:
        results = {}

        keys = [('ally', 'danger'), ('ally', 'opportunity'), ('enemy', 'danger'), ('enemy', 'opportunity')]
        for key in keys:
            name, attr = key
            if name == 'ally':
                base = getattr(ally, attr)
            else:
                base = getattr(enemy, attr)
            results[key] = base * cls.multipliers[key]
        raw = sorted(results.items(), key=lambda x: x[1], reverse=True)
        return [thing[0] for thing in raw]

    def get_action(self, ally: DangerOpportunity, enemy: DangerOpportunity) -> CompositeActionPack:
        raise NotImplementedError


class WanderAndFight(Strategy):
    multipliers = {
        ('ally', 'danger'): 10,
        ('ally', 'opportunity'): 3,
        ('enemy', 'danger'): 0,
        ('enemy', 'opportunity'): 7
    }

    def __init__(self, unit_view):
        super(WanderAndFight, self).__init__(unit_view)

    def get_action(self, ally, enemy):
        """
        if enemy in sight:
            go to enemy
        else:
            if action do thing
        """

        primary = CompositeAction(Action.ATTACK, Target.ENEMY, 0)
        secondary = CompositeAction(action=Action.MOVE, target=Target.ENEMY|Target.HIGHEST|Target.CONCENTRATION,
                                    floor=self.unit_view.attack_action_pts)
        tertiary = CompositeAction(Action.STAY, Target.NULL, 0)
        return CompositeActionPack(primary, secondary, tertiary)
