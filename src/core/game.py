from src.contestants.manager import load_contestants
from src.contestants.grouped_contestant import GroupedContestants
from src.contestants.contestant import Contestant
from src.events import Fight, FindItems
from src.logger import Logger

class Game:
    def __init__(self, logger_state: bool = True):
        self.fights = 0
        self.logger = Logger(logger_state)
        self.gc = GroupedContestants(self.logger)

        # Initialize the game
        self.setup()

    def setup(self) -> None:
        """Initialize contestants and game events."""
        contestants = load_contestants("c.json")
        self.gc.add_contestants(contestants)

        self.fight = Fight(self.gc)
        self.search = FindItems(self.gc)

    def run(self) -> tuple[Game, int]:
        """Run the game until it ends."""
        while self.gc.count_alive() > 1:
            self.search.search()
            self.fight.fight()
            self.fights += 1

        return self.gc, self.fights, self.get_winner()

    def get_winner(self) -> Contestant | None:
        """Determine and return the winner, if any."""
        winners = self.gc.alive_contestants()

        if winners:
            self.gc.logger.won(winners[0])
            return winners[0]
        else:
            self.gc.logger.no_win()
            return None
