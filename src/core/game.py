from __future__ import annotations
from typing import TYPE_CHECKING
from time import sleep
import random
from src.contestants.manager import load_contestants
from src.contestants.grouped_contestant import GroupedContestants
from src.actions import Fight, Scavenge
from src.actions.choices import ActionChoice
from src.logger import Logger, LogLevel
from src.core.map import Position, WorldMap
from src.visualization.map_renderer import run_renderer, MapRenderer
from copy import copy

if TYPE_CHECKING:
    from src.contestants.contestant import Contestant

class Game:
    def __init__(self, logger_state: bool | LogLevel = LogLevel.INFO):
        self.fights = 0
        self.events = []
        if isinstance(logger_state, bool):
            logger_level = LogLevel.INFO if logger_state else LogLevel.QUIET
        else:
            logger_level = LogLevel(logger_state)
        self.logger = Logger(logger_level)
        self.gc = GroupedContestants(self.logger)
        self.time = 0
        self.world_map = WorldMap(10, 10)

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

        if event == ActionChoice.Base.FIGHT:
            self.fights += 1

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
        self.gc.add_contestants(contestants, self.world_map)
        self.renderer = MapRenderer(self.world_map, tick_duration=0.1)

    def run(self) -> tuple[GroupedContestants, int, Contestant | None]:
        """Run the game until it ends."""
        while self.gc.count_alive() > 1:
            self.maintain_events()

            if self.gc.count_alive() <= 1:
                break

            for c in self.gc.get_alive_contestants():
                c.move_random_dir()
                self.world_map.update_position(c, c.position)

            decisions = self.get_decisions()
            self.assign_fighters(decisions[ActionChoice.Base.FIGHT])
            self.assign_looters(decisions[ActionChoice.Base.LOOT])

            if not self.renderer.update_renderer():
                break

            self.time += 1
            # run_renderer(self.world_map, 64)

        return self.gc, self.fights, self.get_winner()

    def assign_fighters(self, fighters_orig):
        fighters = copy(fighters_orig)
        for _ in range(len(fighters) // 2):
            random.shuffle(fighters)
            fighter_a = fighters.pop()
            fighter_b = fighters.pop()

            self.event_initializer(ActionChoice.Base.FIGHT, (fighter_a, fighter_b))

    def assign_looters(self, looters_orig):
        looters =  copy(looters_orig)
        for _ in range(len(looters)):
            random.shuffle(looters)
            looter = looters.pop()
    
            self.event_initializer(ActionChoice.Base.LOOT, (looter,))

    def get_decisions(self) -> list[ActionChoice.Base]:
        decisions = {}
        for c in self.gc.get_available_contestants():
            decisions[c] = c.get_decision_base()

        # return decisions
        grouped_decisions = {}

        for action in ActionChoice.Base:
            grouped_decisions[action] = [c for c, a in decisions.items() if a == action]

        return grouped_decisions

    def get_winner(self) -> Contestant | None:
        """Determine and return the winner, if any."""
        winners = self.gc.get_alive_contestants()

        if winners:
            self.gc.logger.won(winners[0])
            return winners[0]
        else:
            self.gc.logger.no_win()
            return None
