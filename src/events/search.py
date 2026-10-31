from __future__ import annotations

from typing import TYPE_CHECKING

from .event import Event
from random import choices, randint

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant
    from src.contestants.grouped_contestant import GroupedContestants

class FindItems(Event):
    def search(self) -> Contestant:
        """Simulate an item search"""
        game: GroupedContestants = self.gc
        contestant: Contestant = game.random_contestant()
        if not contestant:
            return

        LOOT_TABLE = {
            "NOTHING": {
                "weight": 50,
                "handler": self.got_nothing,
            },
            "FOOD": {
                "weight": 20,
                "handler": self.apply_food,
            },
            "WEAPON": {
                "weight": 15,
                "handler": self.apply_weapon,
            },
            "ARMOR": {
                "weight": 10,
                "handler": self.apply_armor,
            },
            "MEDKIT": {
                "weight": 5,
                "handler": self.apply_medkit,
            },
        }
        
        loot = choices(list(LOOT_TABLE.keys()), weights=[v['weight'] for v in LOOT_TABLE.values()])[0]
        return LOOT_TABLE[loot]['handler'](contestant)

    def got_nothing(self, t: Contestant) -> Contestant:
        """Notify that nothing was found."""
        self.logger.found(t, "nothing")
        return t

    def apply_food(self, t: Contestant) -> Contestant:
        """Apply food and notify"""
        self.apply_heal(t, "food", 30, 5)
        return t

    def apply_tool(self, t: Contestant, stat: str) -> Contestant:
        """Apply given tool and notify"""
        old = getattr(t, stat)
        tool_value = choices(range(20), weights=[x**1.5 for x in range(20, 0, -1)])[0]
        self.logger.found(t, stat, tool_value)
        setattr(t, stat, max(old, tool_value))
        return t

    def apply_weapon(self, t: Contestant) -> Contestant:
        """Apply weapon and notify"""
        self.apply_tool(t, "weapon")
        return t

    def apply_armor(self, t: Contestant) -> Contestant:
        """Apply armor and notify"""
        self.apply_tool(t, "armor")
        return t

    def apply_medkit(self, t: Contestant) -> Contestant:
        """Apply medkit and notify"""
        self.apply_heal(t, "medkit", 50, 30)
        return t

    def apply_heal(self, t: Contestant, tool: str, maxhp: int, minhp: int) -> Contestant:
        """Heal the contestant"""
        val = randint(minhp, maxhp)
        self.logger.found(t, tool, val)
        t.heal(val)
        return t
