from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contestants.contestant import Contestant

class Logger:
    def __init__(self, debug: bool = True):
        self.debug = debug

    def _log(self, message: str) -> None:
        if self.debug:
            print(message)

    def death(self, t: Contestant) -> None:
        self._log(f"{t.name} died")

    def run_away(self, t: Contestant) -> None:
        self._log(f"{t.name} ran away.")

    def hit(self, defender: Contestant, attacker: Contestant) -> None:
        self._log(f"{defender.name} was hit by {attacker.name}.")

    def dmg_both(self, t1: Contestant, t2: Contestant) -> None:
        self._log(f"Both {t1.name} and {t2.name} took damage.")

    def fighting(self, t1: Contestant, t2: Contestant) -> None:
        self._log(f"{t1.name} and {t2.name} are fighting.")

    def found(self, t: Contestant, loot: str, units: int = None) -> None:
        if units:
            self._log(f"{t.name} found {loot} of {units} value.")
        else:
            self._log(f"{t.name} found {loot}")
        
    def heal(self, t: Contestant, amt: int) -> None:
        self._log(f"{t.name} healed {amt}. Health: {t.health}")

    def dmg(self, t: Contestant, amt: int) -> None:
        if amt != 0:
            self._log(f"{t.name} took {amt} damage")

    def won(self, t: Contestant) -> None:
        self._log(f"{t.name} won!")

    def no_win(self) -> None:
        self._log("No one won.")

    def chose(self, t, message) -> None:
        self._log(f"{t.name} chose to {message}")