from __future__ import annotations

from typing import TYPE_CHECKING

from src.contestants.contestant import ActionChoice

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant
    from src.core.game import Game

def decide_world(contestant: Contestant, game: Game, choices: list[ActionChoice.World]) -> ActionChoice.World:
    health_fraction = contestant.health / 100

    utilities = {
        ActionChoice.World.LOOT: 1 - health_fraction,
        ActionChoice.World.FIGHT: health_fraction,
    }

    return max(choices, key=utilities.__getitem__)
