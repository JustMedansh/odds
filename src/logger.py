from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant


class LogLevel(IntEnum):
    QUIET = 0
    IMPORTANT = 1
    INFO = 2
    DEBUG = 3


class Logger:
    """Print simulation events at or above the configured importance."""

    def __init__(self, level: LogLevel = LogLevel.INFO):
        self.level = LogLevel(level)

    def _log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        if self.level >= level:
            print(message)

    def death(self, t: Contestant) -> None:
        self._log(f"{t.name} died.", LogLevel.IMPORTANT)

    def run_away(self, t: Contestant) -> None:
        self._log(f"{t.name} fled the fight.")

    def hit(self, defender: Contestant, attacker: Contestant, amount: int) -> None:
        self._log(f"{attacker.name} hit {defender.name} for {amount} damage.")

    def dmg_both(self, t1: Contestant, t2: Contestant) -> None:
        self._log(f"Both {t1.name} and {t2.name} took damage.")

    def fighting(self, t1: Contestant, t2: Contestant) -> None:
        self._log(f"{t1.name} and {t2.name} started fighting.")

    def found(self, t: Contestant, loot: str, units: int | None = None) -> None:
        level = LogLevel.DEBUG if loot.lower() == "nothing" else LogLevel.INFO
        if units is not None:
            self._log(f"{t.name} found {loot} (value {units}).", level)
        else:
            self._log(f"{t.name} found {loot}.", level)

    def heal(self, t: Contestant, amt: int) -> None:
        self._log(f"{t.name} healed {amt}. Health: {t.health}.", LogLevel.DEBUG)

    def dmg(self, t: Contestant, amt: int) -> None:
        if amt != 0:
            self._log(f"{t.name} took {amt} damage. Health: {t.health}.", LogLevel.DEBUG)

    def won(self, t: Contestant) -> None:
        self._log(f"{t.name} won!", LogLevel.IMPORTANT)

    def no_win(self) -> None:
        self._log("No one won.", LogLevel.IMPORTANT)

    def chose(self, t: Contestant, message: str) -> None:
        self._log(f"{t.name} chose to {message}.", LogLevel.DEBUG)
