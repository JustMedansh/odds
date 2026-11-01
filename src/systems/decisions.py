from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.contestants.contestant import ActionChoice
    from src.contestants.contestant import Contestant


def make_decision_world(contestant: Contestant, choices: list[ActionChoice.World] | None = None,) -> ActionChoice.World:
    if choices is None:
        choices = [ActionChoice.World.LOOT, ActionChoice.World.FIGHT, ActionChoice.World.REST]

    health_fraction = contestant.health / 100
    weapon_fraction = min(contestant.weapon / 20, 1)
    armor_fraction = min(contestant.armor / 20, 1)
    strength_fraction = contestant.personality.strength / 10

    gear = (weapon_fraction + armor_fraction) / 2
    readiness = max(gear, strength_fraction)

    utilities = {
        ActionChoice.World.LOOT: 1 - gear,
        ActionChoice.World.FIGHT: health_fraction * readiness,
        ActionChoice.World.REST: 1 - health_fraction,
    }

    weights = [utilities[action] for action in choices]

    if not any(weights):
        return random.choice(choices)

    return random.choices(choices, weights, k=1)[0]
