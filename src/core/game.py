from __future__ import annotations

from typing import TYPE_CHECKING

from src.contestants.manager import load_contestants
from src.contestants.grouped_contestant import GroupedContestants
from src.events import Fight, FindItems
from src.logger import Logger

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

class Game:
    def __init__(self, logger_state: bool = True):
        self.fights = 0
        self.fighting = []
        self.logger = Logger(logger_state)
        self.gc = GroupedContestants(self.logger)
        self.time = 0

        # Initialize the game
        self.setup()

    def maintain_fighting(self, fight_result=None):
        if fight_result is not None:
            c1, c2, resolved = fight_result
            fighters = (c1, c2)
            fighters_in_list = fighters in self.fighting
            if not resolved:
                if not fighters_in_list:
                    self.fighting.append(fighters) 
            else:
                if fighters_in_list:
                    self.fighting.remove(fighters)

    def setup(self) -> None:
        """Initialize contestants and game events."""
        contestants = load_contestants("c.json")
        self.gc.add_contestants(contestants)

        self.fight = Fight(self.gc, self)
        self.search = FindItems(self.gc, self)

    def run(self) -> tuple[Game, int]:
        """Run the game until it ends."""
        while self.gc.count_alive() > 1:
            if len(self.fighting) == 0:
                self.fighting.append(tuple(self.gc.random_group(2)))
                
            self.search.search()
            self.maintain_fighting()

            for c1, c2 in self.fighting.copy():
                result = self.fight.fight(c1, c2)
                self.maintain_fighting(result)

            self.fights += 1
            self.time += 1

        return self.gc, self.fights, self.get_winner()

    def get_winner(self) -> Contestant | None:
        """Determine and return the winner, if any."""
        winners = self.gc.get_alive_contestants()

        if winners:
            self.gc.logger.won(winners[0])
            return winners[0]
        else:
            self.gc.logger.no_win()
            return None
