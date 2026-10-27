from collections import Counter

from src.contestant import random_contestant 
from src.game import Game
from events import Fight, FindItems

GAMES = 10000

def run():
    contestants = random_contestant(5)

    game = Game()
    game.add_contestants(contestants)
    game.logger.debug = False

    fight = Fight(game)
    search = FindItems(game)

    fights = 0

    while game.count_alive() > 1:
        search.search()
        fight.fight()
        fights += 1

    return game, fights


def old_main():
    winners = Counter()

    total_fights = 0
    total_health = 0
    total_weapon = 0
    total_armor = 0

    for _ in range(GAMES):
        game, fights = run()

        total_fights += fights

        alive = game.alive_tributes()

        if not alive:
            winners["No Winner"] += 1
            continue

        winner = alive[0]

        winners[winner.name] += 1
        total_health += winner.health
        total_weapon += winner.weapon
        total_armor += winner.armor

    print("=== Winners ===")
    for name, wins in winners.most_common():
        print(f"{name}: {wins}")

    winners_count = GAMES - winners["No Winner"]

    print("\n=== Statistics ===")
    print(f"Games: {GAMES}")
    print(f"Average fights/game: {total_fights / GAMES:.2f}")

    if winners_count:
        print(f"Average winner health: {total_health / winners_count:.2f}")
        print(f"Average winner weapon: {total_weapon / winners_count:.2f}")
        print(f"Average winner armor : {total_armor / winners_count:.2f}")

def main():
    print(run())

if __name__ == "__main__":
    main()