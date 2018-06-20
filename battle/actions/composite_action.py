from battle.actions.action import Action
from battle.actions.target import Target


class CompositeAction(object):

    @classmethod
    def null_action(cls):
        return cls(Action.NULL, Target.NULL, 0)

    def __init__(self, action: Action, target: Target, floor: int):
        self.action = action
        self.target = target
        self.floor = floor

    def __eq__(self, other):
        if not isinstance(other, CompositeAction):
            return False
        return (self.action, self.target, self.floor) == (other.action, other.target, other.floor)

    def __repr__(self):
        return 'CompositeAction({!r}, {!r}, {!r})'.format(self.action, self.target, self.floor)

    def __hash__(self):
        return hash(repr(self))

    def __bool__(self):
        return self != self.null_action()

