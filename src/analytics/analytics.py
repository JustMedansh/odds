from src.core.simulation import run_simulation
from collections import Counter

def run_statistics() -> None:
    """Runs a set number of simulations and prints a detailed output of statistics"""
    GAMES = 10000
    winners = Counter()
    
    total_fights = 0
    total_health = 0
    total_weapon = 0
    total_armor = 0

    for _ in range(GAMES):
        game, fights = run_simulation()

        total_fights += fights

        alive = game.get_alive_contestants()

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

if __name__ == "__main__":
    run_statistics()