from .tags import StatTags, get_attribute_value
from dataclasses import dataclass, field, fields
from .generation import GenerationBias, generate_value, BIAS_TABLE

def validate_tags(tags: set) -> None:
    """Validate that no conflicting tags are present"""
    targets = {}

    for tag in tags:
        targets.setdefault(tag.bias_target, []).append(tag)

    for group in targets.values():
        if len(group) > 1:
            raise ValueError(f"Conflicting tags: {tuple(group)}")

def generate_attributes(instance: Skills | Personality):
    """Generate attribute values for given instance of Personality or Skills. To be used in __post_init__"""

    validate_tags(instance.tags)

    for attribute in fields(instance):
        if attribute.name == "tags":
            continue

        bias_key = GenerationBias.NORMAL
        low, high = BIAS_TABLE[bias_key]

        setattr(
            instance,
            attribute.name,
            generate_value(low, high, bias_key)
        )

@dataclass
class Stats:
    """A record of the physical/social/cognitive abilities of a contestant. Determines the success of an action."""
    strength: float | StatTags.Attribute.Strength
    intelligence: float | StatTags.Attribute.Intelligence
    social: float | StatTags.Attribute.Social
    perception: float = field(init=False)
    agility: float = field(init=False)
    survivability: float = field(init=False)
    offensive_power: float = field(init=False)

    def __post_init__(self):
        # Attributes
        self._validate_attribute("strength", StatTags.Attribute.Strength)
        self._validate_attribute("intelligence", StatTags.Attribute.Intelligence)
        self._validate_attribute("social", StatTags.Attribute.Social)

        # Specialized
        self.perception = (self.intelligence * 0.8) + (self.social * 0.2)
        self.survivability = (self.intelligence * 0.2) + (self.strength * 0.2)
        self.agility = (self.intelligence * 0.7) + (self.strength * 0.3)
        self.offensive_power = (self.intelligence * 0.25) + (self.strength * 0.75)

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
    impulsiveness: int = field(init=False)
    curiosity: int = field(init=False)
    aggression: int = field(init=False)
    courage: int = field(init=False)

    def __post_init__(self):
        generate_attributes(self)

@dataclass 
class Skills:
    """Affects proficiency at specific actions. Skills are learnable."""    
    tags: set = field(default_factory=set)

    cooking: int = field(init=False)
    healing: int = field(init=False)
    stealth: int = field(init=False) # stealth
    craftsmanship: int = field(init=False) # manipulating env, makeshift, improvisation
    engineering: int = field(init=False) # mechanics and electrical
    aiming: int = field(init=False) # increases accuracy with ranged projectile.
    fishing: int = field(init=False)
    scavenging: int = field(init=False)
    trapping: int = field(init=False)
    fire_starting: int = field(init=False)
    swimming: int = field(init=False)

    def __post_init__(self):
        generate_attributes(self)
