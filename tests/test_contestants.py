import pytest

from src.contestants import Contestant, StatTags, Stats, get_attribute_value, random_contestant


@pytest.mark.parametrize(
    ("tag", "attribute", "expected"),
    [
        (StatTags.Attribute.Strength.HIGH, "strength", 7),
        (StatTags.Attribute.Intelligence.LOW, "intelligence", 3),
        (StatTags.Attribute.Social.VERY_HIGH, "social", 9),
    ],
)
def test_stats_resolves_attribute_tags(monkeypatch, tag, attribute, expected):
    monkeypatch.setattr("src.contestants.attributes.get_attribute_value", lambda _: expected)

    stats = Stats(strength=tag if attribute == "strength" else 5,
                  intelligence=tag if attribute == "intelligence" else 5,
                  social=tag if attribute == "social" else 5)

    assert getattr(stats, attribute) == expected


def test_stats_calculates_specialized_attributes():
    stats = Stats(strength=8, intelligence=5, social=10)

    assert stats.perception == pytest.approx(6)
    assert stats.survivability == pytest.approx(2.6)
    assert stats.agility == pytest.approx(5.9)


def test_get_attribute_value_uses_tag_range(monkeypatch):
    calls = []

    def fake_uniform(low, high):
        calls.append((low, high))
        return (low + high) / 2

    monkeypatch.setattr("src.contestants.tags.random.uniform", fake_uniform)

    value = get_attribute_value(StatTags.Attribute.Intelligence.VERY_HIGH)

    assert calls == [(8, 9.5)]
    assert value == pytest.approx(8.75)


def test_contestant_damage_and_healing_lifecycle():
    contestant = Contestant("Ari", "F", Stats(5, 5, 5))

    contestant.take_damage(30)
    assert contestant.health == 70
    assert contestant.alive is True

    contestant.heal(50)
    assert contestant.health == 100

    contestant.take_damage(125)
    assert contestant.health == 0
    assert contestant.alive is False

    contestant.heal(20)
    assert contestant.health == 0


def test_contestant_string_shows_name_and_health():
    contestant = Contestant("Kai", "M", Stats(5, 5, 5), health=42)

    assert str(contestant) == "Kai: 42"


def test_random_contestant_creates_requested_number_of_valid_contestants():
    contestants = random_contestant(8)

    assert len(contestants) == 8
    assert all(isinstance(contestant, Contestant) for contestant in contestants)
    assert all(contestant.gender in {"M", "F"} for contestant in contestants)
    assert all(
        1 <= value <= 10
        for contestant in contestants
        for value in (contestant.stats.strength, contestant.stats.intelligence, contestant.stats.social)
    )
