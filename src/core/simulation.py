from __future__ import annotations

from typing import TYPE_CHECKING

from src.core.game import Game

if TYPE_CHECKING:
    from src.contestants.grouped_contestant import GroupedContestants

def run_simulation(logger_state: bool = True) -> tuple[GroupedContestants, int]:
    """Run a single simulation of the game, with printing toggled using logger_state."""

    game = Game(logger_state)
    gc, fights, winner = game.run()
    return gc, fights
