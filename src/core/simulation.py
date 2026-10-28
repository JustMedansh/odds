from src.contestants.manager import load_contestants
from src.contestants.grouped_contestant import GroupedContestants
from src.events import Fight, FindItems

def run_simulation(logger_state: bool = True) -> tuple[GroupedContestants, int]:
    """Run a single simulation of the game, with printing toggled using logger_state."""
    contestants = load_contestants('c.json')

    game = GroupedContestants()
    game.add_contestants(contestants)
    game.logger.debug = logger_state

    fight = Fight(game)
    search = FindItems(game)

    fights = 0

    while game.count_alive() > 1:
        search.search()
        fight.fight()
        fights += 1

    winner = game.alive_contestants()
    if len(winner) > 0:
        game.logger.won(winner[0])
    else:
        game.logger.no_win()

    return game, fights