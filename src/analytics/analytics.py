from src.core.simulation import run_simulation
from collections import Counter

def run_statistics(games: int = 10_000, progress_interval: int = 100) -> None:
    """Runs a set number of simulations and prints a detailed output of statistics"""
    if games <= 0:
        raise ValueError("games must be greater than zero")
    if progress_interval <= 0:
        raise ValueError("progress_interval must be greater than zero")

    winners = Counter()
    
    total_fights = 0
    total_health = 0
    total_weapon = 0
    total_armor = 0

    print(f"Running {games} simulations...", flush=True)
    for game_number in range(1, games + 1):
        game, fights, winner = run_simulation(False)

        total_fights += fights

        if game_number % progress_interval == 0 or game_number == games:
            print(f"Simulated {game_number}/{games} games...", flush=True)

        if winner is None:
            winners["No Winner"] += 1
            continue

        winners[winner.name] += 1
        total_health += winner.health
        total_weapon += winner.weapon
        total_armor += winner.armor

    print("=== Winners ===")
    for name, wins in winners.most_common():
        print(f"{name}: {wins}")

    winners_count = games - winners["No Winner"]

    print("\n=== Statistics ===")
    print(f"Games: {games}")
    print(f"Average fights/game: {total_fights / games:.2f}")

    if winners_count:
        print(f"Average winner health: {total_health / winners_count:.2f}")
        print(f"Average winner weapon: {total_weapon / winners_count:.2f}")
        print(f"Average winner armor : {total_armor / winners_count:.2f}")

if __name__ == "__main__":
    run_statistics()
