import json
from pathlib import Path

from src.contestants.contestant import Contestant


def get_path(filename: str) -> Path:
    """Get path of file from filename."""
    return Path(__file__).resolve().parent.parent.parent / "data" / filename


def load_contestants(filename: str) -> list[Contestant]:
    """Load contestant profiles from the JSON file."""
    path = get_path(filename)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        Contestant(
            name=item["name"],
            gender=item["gender"],
            skills=item["skills"],
        )
        for item in data
    ]


def save_contestant(filename: str, contestant: dict) -> None:
    """Save a contestant to the JSON file."""
    path = get_path(filename)

    if path.exists() and path.stat().st_size > 0:
        with path.open("r", encoding="utf-8") as file:
            contestants = json.load(file)
    else:
        contestants = []

    contestants.append(contestant)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(contestants, file, indent=4)


def adding_interface(filename: str) -> None:
    contestant = {
        "name": input("Name: "),
        "gender": input("Gender (M/F): "),
        "skills": {
            "strength": int(input("Strength (1-10): ")),
            "intelligence": int(input("Intelligence (1-10): ")),
            "social": int(input("Social (1-10): ")),
        },
    }

    save_contestant(filename, contestant)


def main() -> None:
    print("CONTESTANT MANAGER")
    filename = "c.json"

    while True:
        adding_interface(filename)


if __name__ == "__main__":
    main()
