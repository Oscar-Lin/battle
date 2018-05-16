from battle.actions.action_package import ActionPackage
from battle.actions.target import Target
from battle.actions.temp_action_thingy import TempAction


class TempStrategy(object):

    def __init__(self, primary: ActionPackage, secondary: ActionPackage, tertiary: ActionPackage):
        self.primary = primary
        self.secondary = secondary
        self.tertiary = tertiary

    def get_next_action(self, unit):
        pts = unit.get_action_pts()
        if self.primary.floor < pts:
            return self.primary.action
        elif self.secondary.floor < pts:
            return self.secondary.action
        else:
            return self.tertiary.action
    """if ... then... return ..."""








