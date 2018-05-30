from battle.actions.action import Action
from battle.actions.target import Target


class CompositeAction(object):
    def __init__(self, action: Action, target: Target, floor: int):
        self.action = action
        self.target = target
        self.floor = floor


