from __future__ import annotations
from typing import TYPE_CHECKING
from time import sleep
import random
from src.contestants.manager import load_contestants
from src.contestants.grouped_contestant import GroupedContestants
from src.actions import Fight, Scavenge
from src.actions.choices import ActionChoice
from src.logger import Logger

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

class Game:
    def __init__(self, logger_state: bool = True):
        self.fights = 0
        self.events = []
        self.logger = Logger(logger_state)
        self.gc = GroupedContestants(self.logger)
        self.time = 0

        self.fighters = []

        # Initialize the game
        self.setup()

    def event_initializer(self, event: ActionChoice.Base, contestants: tuple[Contestant]):
        event_dispatcher = {
            ActionChoice.Base.FIGHT: Fight,
            ActionChoice.Base.LOOT: Scavenge,
        }

        event_class = event_dispatcher[event]
        active_event = event_class(self.gc, self, list(contestants))
        self.events.append(active_event)

        for contestant in contestants:
            contestant.busy = True

        if event == ActionChoice.Base.FIGHT:
            self.logger.fighting(*contestants)

    def maintain_events(self):
        for event in self.events.copy():
            if event.update():
                self.events.remove(event)
                for contestant in event.contestants:
                    contestant.busy = False

    def setup(self) -> None:
        """Initialize contestants and game events."""
        contestants = load_contestants("c.json")
        self.gc.add_contestants(contestants)

    def run(self) -> tuple[Game, int]:
        """Run the game until it ends."""
        while self.gc.count_alive() > 1:
            self.maintain_events()

            if self.gc.count_alive() <= 1:
                break

            # has_fight = any(isinstance(event, Fight) for event in self.events)
            # if not has_fight and len(available) >= 2:
            #     c1, c2 = self.gc.random_group(2)
            #     self.event_initializer(ActionChoice.Base.FIGHT, (c1, c2))

            # available = self.gc.get_available_contestants()
            # if available and False:
            #     contestant = self.gc.random_contestant()
            #     self.event_initializer(ActionChoice.Base.LOOT, (contestant,))

            # self.fights += 1

            decisions = self.get_decisions()
            self.fighters = [contestant for contestant, action in decisions.items() if action == ActionChoice.Base.FIGHT]
            self.assign_fighters()

            self.time += 1

        return self.gc, self.fights, self.get_winner()

    def assign_fighters(self):
        for _ in range(len(self.fighters) // 2):
            random.shuffle(self.fighters)
            fighter_a = self.fighters.pop()
            fighter_b = self.fighters.pop()

            self.event_initializer(ActionChoice.Base.FIGHT, (fighter_a, fighter_b))

    def get_decisions(self) -> list[ActionChoice.Base]:
        decisions = {}
        for c in self.gc.get_available_contestants():
            decisions[c] = c.get_decision_world()

        return decisions

    def get_winner(self) -> Contestant | None:
        """Determine and return the winner, if any."""
        winners = self.gc.get_alive_contestants()

        if winners:
            self.gc.logger.won(winners[0])
            return winners[0]
        else:
            self.gc.logger.no_win()
            return None
