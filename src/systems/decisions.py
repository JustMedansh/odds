from __future__ import annotations

from typing import TYPE_CHECKING

from src.contestants.contestant import Action

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant
    from src.core.game import Game

def decide_world(contestant: Contestant, game: Game, choices: list[Action.World]) -> Action.World:
    health_fraction = contestant.health / 100

    utilities = {
        Action.World.LOOT: 1 - health_fraction,
        Action.World.FIGHT: health_fraction,
    }

    return max(choices, key=utilities.__getitem__)
