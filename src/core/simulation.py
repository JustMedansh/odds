from __future__ import annotations

from typing import TYPE_CHECKING

from src.core.game import Game
from src.logger import LogLevel

if TYPE_CHECKING:
    from src.contestants.grouped_contestant import GroupedContestants

def run_simulation(logger_state: bool | LogLevel = LogLevel.INFO) -> tuple[GroupedContestants, int]:
    """Run one simulation, optionally selecting its logger verbosity."""

    game = Game(logger_state)
    gc, fights, winner = game.run()
    return gc, fights
