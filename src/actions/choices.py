from enum import Enum, auto
import random

class ActionChoice:
    class Base(Enum):
        LOOT = auto()
        COMBAT = auto()
        REST = auto()

    class Combat:
        class Offensive(Enum):
            ATTACK = auto()

        class Defensive(Enum):
            DEFEND = auto()
            DODGE = auto()

        class GameEnding(Enum):
            FLEE = auto()
