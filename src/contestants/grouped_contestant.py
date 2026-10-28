from src.logger import Logger
from src.contestants.contestant import Contestant
import random

class GroupedContestants:
    def __init__(self):
        # contestants -> group of contestants
        self.contestants = {}
        self.day = 1
        self.next_id = 1
        self.logger = Logger()

    def add_contestants(self, contestants: list[Contestant]) -> None:
        """Add a list of contestants"""
        for contestant in contestants:
            contestant.logger = self.logger
            self.contestants[self.next_id] = contestant
            self.next_id += 1

    def add_contestant(self, contestant: Contestant) -> None:
        """Add a contestant"""
        contestant.logger = self.logger
        self.contestants[self.next_id] = contestant
        self.next_id += 1

    def get_contestant(self, id: int) -> Contestant:
        """Return a contestant with their id"""
        return self.contestants[id]

    def get_all_contestants(self) -> dict[int, Contestant]:
        """Return a dict of all the contestants"""
        return self.contestants

    def alive_contestants(self) -> list[Contestant]:
        """Return a list of alive contestants"""
        return [
            contestant
            for contestant in self.contestants.values()
            if contestant.alive
        ]

    def dead_contestants(self) -> list[Contestant]:
        """Return a list of dead contestants"""
        return [
            contestant
            for contestant in self.contestants.values()
            if not contestant.alive
        ]

    def random_contestant(self) -> Contestant:
        """Return a random contestant from alive contestants."""
        return random.choice(self.alive_contestants())

    def random_group(self, number_of_contestants: int) -> list[Contestant]:
        """Return a random group of contestants from alive contestants."""
        return random.sample(
            self.alive_contestants(),
            k=number_of_contestants
        )

    def count_dead(self) -> int:
        """Return number of dead contestants"""
        return len(self.dead_contestants())

    def count_alive(self) -> int:
        """Return number of alive contestants"""
        return len(self.alive_contestants())