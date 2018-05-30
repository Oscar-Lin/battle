from battle.actions.temp_action_thingy import TempAction
from battle.actions.target import Target


class ActionPackage(object):
    def __init__(self, action: TempAction, target: Target, floor: int):
        self.action = action
        self.target = target
        self.floor = floor


