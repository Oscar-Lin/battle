

class UnitView(object):
    """
    returns the state of a unit
    """
    def __init__(self, unit):
        self._unit = unit
        
    @property
    def health(self) -> int:
        return self._unit.get_health()
        
    @property
    def available_action_pts(self) -> int:
        return self._unit.get_action_points()
        
    @property
    def attack_action_pts(self) -> int:
        return self._unit.get_weapon().action_pts
        
    @property
    def sight_range(self) -> int:
        return self._unit.get_sight_range()
        
    @property
    def weapon_range(self) -> int:
        return self._unit.get_weapon().range
        
    @property
    def perimeter_range(self) -> int:
        return self._unit.get_perimeter_size()
        
    @property
    def uses_melee_weapon(self) -> bool:
        return self._unit.get_weapon().is_melee_weapon()
