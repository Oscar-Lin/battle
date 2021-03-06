import random
from typing import List

from battle.maptools.footprint import DangerOpportunity
from battle.players.action import Action


class Strategy(object):
    def __init__(self):
        pass

    def get_action(self, ally: DangerOpportunity, enemy: DangerOpportunity) -> List[Action]:
        raise NotImplementedError


class StupidStrategy(Strategy):
    def __init__(self):
        super(StupidStrategy, self).__init__()

    def get_action(self, ally, enemy):
        actions = Action.to_list()
        random.shuffle(actions)
        return actions
