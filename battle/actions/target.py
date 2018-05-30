from enum import Flag, auto


class Target(Flag):
    NULL = 0

    ENEMY = auto()
    ALLY = auto()

    NEAREST = auto()
    FURTHEST = auto()

    STRONGEST = auto()
    WEAKEST = auto()

    HIGHEST = auto()
    LOWEST = auto()

    HEALTH = auto()
    WEAPON = auto()
    CONCENTRATION = auto()

    OPPORTUNITY = auto()
    DANGER = auto()

    ADVANTAGE = auto()

    def has_any(self, other: "Target"):
        return bool(self & other)

    def has_only(self, other: "Target"):
        return self == other

    def has_at_least(self, other: "Target"):
        return (self & other) == other

    @classmethod
    def to_list(cls):
        return sorted(cls.__members__.values(), key= lambda action: action.name)