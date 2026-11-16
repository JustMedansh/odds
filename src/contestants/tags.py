from enum import StrEnum, auto
import random

class StatTags:
    """Tags that can affect the stats of a contestant"""
    class Attribute:
        """Tags that can be used in place of numeric values"""
        class Strength(StrEnum):
            VERY_LOW = auto()
            LOW = auto()
            AVERAGE = auto()
            HIGH = auto()
            VERY_HIGH = auto()

        class Intelligence(StrEnum):
            VERY_LOW = auto()
            LOW = auto()
            AVERAGE = auto()
            HIGH = auto()
            VERY_HIGH = auto()

        class Social(StrEnum):
            VERY_LOW = auto()
            LOW = auto()
            AVERAGE = auto()
            HIGH = auto()
            VERY_HIGH = auto()

    class Specialized(StrEnum):
        """Tags that change derived values"""
        CHEF = auto()
        MEDIC = auto()

def get_attribute_value(tag: StrEnum) -> float:
    """Return a random value for attribute type (very low, low, ...)"""

    ATTRIBUTE_TABLE = {
        "very_low": (0.5, 2),
        "low": (2, 4),
        "average": (4, 6),
        "high": (6, 8),
        "very_high": (8, 9.5)
    }

    return random.uniform(*ATTRIBUTE_TABLE[tag.value])