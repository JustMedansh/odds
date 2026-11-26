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
        CHEF = (auto(), GenerationBias.HIGH, "cooking")
        MEDIC = (auto(), GenerationBias.HIGH, "healing")
        SNEAK = (auto(), GenerationBias.HIGH, "stealth")
        CRAFTSMAN = (auto(), GenerationBias.HIGH, "craftsmanship")
        ENGINEER = (auto(), GenerationBias.HIGH, "engineering")
        MARKSMAN = (auto(), GenerationBias.HIGH, "aiming")
        FISHER = (auto(), GenerationBias.HIGH, "fishing")
        SCAVENGER = (auto(), GenerationBias.HIGH, "scavenging")
        TRAPPER = (auto(), GenerationBias.HIGH, "trapping") 
        FIRE_STARTER = (auto(), GenerationBias.HIGH, "fire_starting")
        SWIMMER = (auto(), GenerationBias.HIGH, "swimming")

        def __new__(cls, value, bias_type, bias_target):
            obj = str.__new__(cls, value)
            obj._value_ = value
            obj.bias_type = bias_type
            obj.bias_target = bias_target
            return obj

    class PersonalityTraits(StrEnum):
        """Tags that affect Personality"""
        # (bias type, bias target)

        # --- NON PAIRED ---
        SELFLESS = (auto(), GenerationBias.HIGH, "selflessness")
        CAUTION = (auto(), GenerationBias.HIGH, "caution")
        RECKLESS = (auto(), GenerationBias.HIGH, "impulsiveness")
        CURIOUS = (auto(), GenerationBias.HIGH, "curiosity")

        # --- PAIRED ---
        LONER = (auto(), GenerationBias.LOW, "sociability")
        SOCIALISER = (auto(), GenerationBias.HIGH, "sociability")

        SUBMISSIVE = (auto(), GenerationBias.LOW, "assertiveness")
        DOMINANT = (auto(), GenerationBias.HIGH, "assertiveness")

        INSENSITIVE = (auto(), GenerationBias.LOW, "empathy")
        CARING = (auto(), GenerationBias.HIGH, "empathy")

        PASSIVE = (auto(), GenerationBias.LOW, "aggression")
        AGGRESSIVE = (auto(), GenerationBias.HIGH, "aggression")

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