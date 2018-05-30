from battle.actions.composite_action import CompositeAction
from battle.actions.target import Target
from battle.actions.action import Action


class ActionPack(object):

    def __init__(self, primary: CompositeAction, secondary: CompositeAction, tertiary: CompositeAction):
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








