from enum import StrEnum, auto
from .generation import generate_value, GenerationBias
import random

class StatTags:
    """Tags that can affect the stats of a contestant"""
    class Attribute:
        """Tags that affect Stats"""
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

    class SkillTraits(StrEnum):
        """Tags that affect Skills"""
        # (bias type, bias target)
        CHEF = ("chef", GenerationBias.HIGH, "cooking")
        MEDIC = ("medic", GenerationBias.HIGH, "healing")

        def __new__(cls, value, bias_type, bias_target):
            obj = str.__new__(cls, value)
            obj._value_ = value
            obj.bias_type = bias_type
            obj.bias_target = bias_target
            return obj

    class PersonalityTraits(StrEnum):
        """Tags that affect Personality"""
        # (bias type, bias target)
        INTROVERT = (auto(), GenerationBias.LOW, "sociability")
        EXTROVERT = (auto(), GenerationBias.HIGH, "sociability")

        SUBMISSIVE = (auto(), GenerationBias.LOW, "assertiveness")
        DOMINANT = (auto(), GenerationBias.HIGH, "assertiveness")

        SELFLESS = (auto(), GenerationBias.HIGH, "selflessness")

        CARING = (auto(), GenerationBias.HIGH, "selflessness")
        INSENSITIVE = (auto(), GenerationBias.HIGH, "selflessness")

        CAUTION = (auto(), GenerationBias.HIGH, "selflessness")
        RECKLESS = (auto(), GenerationBias.HIGH, "selflessness")
        CURIOUS = (auto(), GenerationBias.HIGH, "selflessness")

        AGGRESSIVE = (auto(), GenerationBias.HIGH, "selflessness")
        PASSIVE = (auto(), GenerationBias.HIGH, "selflessness")

        COWARD = (auto(), GenerationBias.LOW, "courage")
        BRAVE = (auto(), GenerationBias.HIGH, "courage")

        def __new__(cls, value, bias_type, bias_target):
            obj = str.__new__(cls, value)
            obj._value_ = value
            obj.bias_type = bias_type
            obj.bias_target = bias_target
            return obj

def get_attribute_value(tag: StrEnum) -> float:
    """Return a random value for attribute type (very low, low, ...)"""

    ATTRIBUTE_TABLE = {
        "very_low": (1, 2),
        "low": (2, 4),
        "average": (4, 6),
        "high": (6, 8),
        "very_high": (8, 9.5)
    }

    return random.uniform(*ATTRIBUTE_TABLE[tag.value])