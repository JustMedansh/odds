from __future__ import annotations

import random
from typing import TYPE_CHECKING
from src.actions.choices import ActionChoice

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant


def make_decision_world(contestant: Contestant, choices: list[ActionChoice.Base] | None = None,) -> ActionChoice.Base:
    if choices is None:
        choices = [ActionChoice.Base.LOOT, ActionChoice.Base.FIGHT, ActionChoice.Base.REST]

    health_fraction = contestant.health / 100
    weapon_fraction = min(contestant.weapon / 20, 1)
    armor_fraction = min(contestant.armor / 20, 1)
    strength_fraction = contestant.personality.strength / 10

    gear = (weapon_fraction + armor_fraction) / 2
    readiness = max(gear, strength_fraction)

    utilities = {
        ActionChoice.Base.LOOT: 1 - gear,
        ActionChoice.Base.FIGHT: health_fraction * readiness,
        ActionChoice.Base.REST: 1 - health_fraction,
    }

    weights = [utilities[action] for action in choices]

    if not any(weights):
        return random.choice(choices)

    return random.choices(choices, weights, k=1)[0]
    return random.choice([ActionChoice.Base.FIGHT, ActionChoice.Base.LOOT])
