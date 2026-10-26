class Logger:
    def __init__(self):
        self.debug = True

    def _log(self, message):
        if self.debug:
            print(message)

    def death(self, t):
        self._log(f"{t.name} was killed.")

    def run_away(self, t):
        self._log(f"{t.name} ran away.")

    def hit(self, attacker, defender):
        self._log(f"{defender.name} was hit by {attacker.name}.")

    def dmg_both(self, t1, t2):
        self._log(f"Both {t1.name} and {t2.name} took damage.")

    def fighting(self, t1, t2):
        self._log(f"{t1.name} and {t2.name} are fighting.")

    def found(self, t, loot, units=None):
        if units:
            self._log(f"{t.name} found {loot} of {units} value.")
        else:
            self._log(f"{t.name} found {loot}")
        
    def healed(self, t, amt):
        self._log(f"{t.name} healed {amt}. Health: {t.health}")

    def recieved_damage(self, t, amt):
        self._log(f"{t.name} took {amt} damage")