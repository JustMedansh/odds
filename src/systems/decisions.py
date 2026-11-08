from __future__ import annotations

import random
from typing import TYPE_CHECKING
from src.actions.choices import ActionChoice
from typing import NamedTuple

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

class DecisionStats(NamedTuple):
    health_fraction: float
    weapon_fraction: float
    armor_fraction: float
    strength_fraction: float
    agility_fraction: float
    gear: float
    readiness: float

def get_decision_stats(contestant: Contestant) -> DecisionStats:
    """Return a DecisionStats object containing the required stats"""
    health_fraction = contestant.health / 100
    weapon_fraction = min(contestant.weapon / 20, 1)
    armor_fraction = min(contestant.armor / 20, 1)
    strength_fraction = contestant.personality.strength / 10
    agility_fraction = contestant.personality.agility

    gear = (weapon_fraction + armor_fraction) / 2
    readiness = max(gear, strength_fraction)

    return DecisionStats(
        health_fraction=health_fraction,
        weapon_fraction=weapon_fraction,
        armor_fraction=armor_fraction,
        strength_fraction=strength_fraction,
        agility_fraction=agility_fraction,
        gear=gear,
        readiness=readiness
    )

def add_noise(stats: DecisionStats, amount: float = 0.1) -> DecisionStats:
    return stats._replace(**{
        field: max(0, min(1, getattr(stats, field) + random.uniform(-amount, amount)))
        for field in stats._fields
    })

def make_decision_base(contestant: Contestant, choices: list[ActionChoice.Base] | None = None) -> ActionChoice.Base:
    """Returns a decision according to ActionChoice.Base"""
    if choices is None:
        choices = [ActionChoice.Base.LOOT, ActionChoice.Base.FIGHT, ActionChoice.Base.REST]

    stats = get_decision_stats(contestant)
    stats = add_noise(stats)

    utilities = {
        ActionChoice.Base.LOOT: 1 - stats.gear,
        ActionChoice.Base.FIGHT: stats.health_fraction * stats.readiness,
        ActionChoice.Base.REST: 1 - stats.health_fraction,
    }

    weights = [utilities[action] for action in choices]

    if not any(weights):
        return random.choice(choices)

    return random.choices(choices, weights, k=1)[0]

def make_decision_fight(contestant: Contestant, choices: list[ActionChoice.Fight] | None = None) -> ActionChoice.Fight:
    """Returns a decision according to ActionChoice.Fight"""
    if choices is None:
        choices = [ActionChoice.Fight.ATTACK, ActionChoice.Fight.DEFEND, ActionChoice.Fight.DODGE, ActionChoice.Fight.FLEE]
    
    stats = get_decision_stats(contestant)
    stats = add_noise(stats)

    utilities = {
        ActionChoice.Fight.ATTACK: stats.readiness,
        ActionChoice.Fight.DEFEND: stats.armor_fraction, 
        ActionChoice.Fight.DODGE: stats.agility_fraction, 
        ActionChoice.Fight.FLEE: (1 - stats.health_fraction) / 1.5
    }

    weights = [utilities[action] for action in choices]

    if not any(weights):
        return random.choice(choices)

    return random.choices(choices, weights, k=1)[0]