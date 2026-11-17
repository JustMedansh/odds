import random
from .tags import StatTags, get_attribute_value
from dataclasses import dataclass, field
from enum import Enum, auto

class GenerationBias(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()

def generate_value(minimum: int, maximum: int, bias: GenerationBias) -> float:
    values = range(minimum, maximum)
    weights = generate_weights(minimum, maximum, bias)

    return random.choices(values, weights, k=1)[0]

def generate_weights(minimum: int, maximum: int, bias: GenerationBias) -> float:
    count = maximum - minimum + 1

    if bias == GenerationBias.NORMAL:
        midpoint = (count - 1) / 2
        weights = [count - abs(i - midpoint) for i in range(count)]

    elif bias == GenerationBias.LOW:
        weights = list(range(count, 0, -1))

    elif bias == GenerationBias.HIGH:
        weights = list(range(1, count + 1))

    return weights

@dataclass
class Stats:
    """A record of the physical/social/cognitive abilities of a contestant. Determines the success of an action."""
    strength: float | StatTags.Attribute.Strength
    intelligence: float | StatTags.Attribute.Intelligence
    social: float | StatTags.Attribute.Social
    perception: float = field(init=False)
    agility: float = field(init=False)
    survivability: float = field(init=False)

    def __post_init__(self):
        # Attributes
        self._validate_attribute("strength", StatTags.Attribute.Strength)
        self._validate_attribute("intelligence", StatTags.Attribute.Intelligence)
        self._validate_attribute("social", StatTags.Attribute.Social)

        # Specialized
        self.perception = (self.intelligence * 0.8) + (self.social * 0.2)
        self.survivability = (self.intelligence + self.strength) * 0.5
        self.agility = (self.intelligence * 0.7) + (self.strength * 0.3)

    def _validate_attribute(self, name: str, tag: type[StatTags.Attribute]) -> None:
        value = getattr(self, name)

        if isinstance(value, tag):
            value = get_attribute_value(value)
            setattr(self, name, value)

        if not 1 <= value <= 10:
            raise ValueError(f"{name} must be between 1 and 10, current value {value}")

@dataclass 
class Personality:
    """Affects decision making of actions"""    
    tags: set = field(default_factory=set)

    sociability: int = field(init=False)
    assertiveness: int = field(init=False)
    selflessness: int = field(init=False)
    empathy: int = field(init=False)
    caution: int = field(init=False)
    impulsivity: int = field(init=False)
    curiosity: int = field(init=False)
    aggression: int = field(init=False)

    def __post_init__(self):
        ...