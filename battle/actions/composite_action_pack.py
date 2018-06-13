from battle.actions.composite_action import CompositeAction


class CompositeActionPack(object):

    def __init__(self, primary: CompositeAction, secondary: CompositeAction, tertiary: CompositeAction):
        self.primary = primary
        self.secondary = secondary
        self.tertiary = tertiary
        self._current_action = self.primary
        self._current_action_points = None  # type: int
        self._previous_action_points = None  # type: int

    def get_next_action(self, available_action_pts) -> CompositeAction:
        self._previous_action_points = self._current_action_points
        self._current_action_points = available_action_pts

        if self._current_action == CompositeAction.null_action():
            return self._current_action

        if self.did_previous_action_fail():

            if self._current_action == self.primary:
                if self.secondary.floor <= available_action_pts:
                    self._current_action = self.secondary
                elif self.tertiary.floor <= available_action_pts:
                    self._current_action = self.tertiary
                else:
                    self._current_action = CompositeAction.null_action()

            elif self._current_action == self.secondary:
                if self.tertiary.floor <= available_action_pts:
                    self._current_action = self.tertiary
                else:
                    self._current_action = CompositeAction.null_action()

            else:
                self._current_action = CompositeAction.null_action()

        else:
            if self._current_action == self.tertiary:
                if self.tertiary.floor > available_action_pts:
                    self._current_action = CompositeAction.null_action()
                    
            else:
                if self.primary.floor <= available_action_pts:
                    self._current_action = self.primary
                elif self.secondary.floor <= available_action_pts:
                    self._current_action = self.secondary
                elif self.tertiary.floor <= available_action_pts:
                    self._current_action = self.tertiary
                else:
                    self._current_action = CompositeAction.null_action()

        return self._current_action

    def did_previous_action_fail(self):
        if self._previous_action_points is None:
            return False
        return self._previous_action_points == self._current_action_points






