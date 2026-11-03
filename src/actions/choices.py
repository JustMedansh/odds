from enum import Enum, auto


class ActionChoice:
    class Base(Enum):
        LOOT = auto()
        FIGHT = auto()
        REST = auto()

    class Fight(Enum):
        ATTACK = auto()
        DEFEND = auto()
        DODGE = auto()
        FLEE = auto()
