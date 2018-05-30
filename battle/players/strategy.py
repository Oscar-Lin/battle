import random
from typing import List

from battle.maptools.footprint import DangerOpportunity
from battle.actions.action_pack import ActionPack


class Strategy(object):
    def __init__(self):
        pass

    def get_action(self, ally: DangerOpportunity, enemy: DangerOpportunity):
        raise NotImplementedError


class StupidStrategy(Strategy):
    def __init__(self):
        super(StupidStrategy, self).__init__()

    def get_action(self, ally, enemy):
        actions = ActionPack('oops', 'i', 'orangutan')
        return actions
