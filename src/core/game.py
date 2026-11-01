from __future__ import annotations
from typing import TYPE_CHECKING

from src.contestants.manager import load_contestants
from src.contestants.grouped_contestant import GroupedContestants
from src.actions import Fight, FindItems
from src.logger import Logger
from src.contestants.contestant import ActionChoice

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

class Game:
    def __init__(self, logger_state: bool = True):
        self.fights = 0
        self.events = []
        self.logger = Logger(logger_state)
        self.gc = GroupedContestants(self.logger)
        self.time = 0

        # Initialize the game
        self.setup()

    def maintain_events(self, event_result: tuple, event_type: ActionChoice):
        if event_result is not None:
            c, t, resolved = event_result
            event = (*c, t, event_type)
            event_in_list = event in self.events

            if event_in_list:
                self.events.remove(event)

            if resolved:
                for contestant in c:
                    contestant.busy = False

            if not resolved:
                if not event_in_list:
                    for contestant in c:
                        contestant.busy = True
                    if event_type == ActionChoice.Fight:
                        self.logger.fighting(*c)
                self.events.append((*c, t + 1, event_type))

    def setup(self) -> None:
        """Initialize contestants and game events."""
        contestants = load_contestants("c.json")
        self.gc.add_contestants(contestants)

        self.fight = Fight(self.gc, self)
        self.search = FindItems(self.gc, self)

    def run(self) -> tuple[Game, int]:
        """Run the game until it ends."""
        while self.gc.count_alive() > 1:
            if len(self.events) == 0:
                try:
                    c1, c2 = self.gc.random_group(2)
                except IndexError:
                    pass
                self.maintain_events(((c1, c2), 0, False), ActionChoice.Fight)
                
            self.search.search()

            for c1, c2, t, state in self.events.copy():
                if state == ActionChoice.Fight:
                    result = self.fight.fight(c1, c2, t)
                    self.maintain_events(result, ActionChoice.Fight)

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
