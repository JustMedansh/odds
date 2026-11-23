import pytest

from src.actions import Action, Attack, Defend, Move
from src.contestants import Contestant, Stats, random_contestant
from src.map.world_map import Position


def test_stats_calculates_offensive_power():
    stats = Stats(strength=8, intelligence=5, social=5)

    assert stats.offensive_power == pytest.approx(7.25)


def test_base_action_tick_runs_without_missing_self_error():
    action = Action(Contestant("Ari", "F", Stats(5, 5, 5)))
    action.duration = None

    action.update()

    assert action.elapsed_time == 1
    assert action.finished is False


def test_move_update_moves_and_consumes_energy():
    contestant = Contestant("Ari", "F", Stats(5, 5, 5))
    action = Move(contestant, direction=0, speed=2)

    action.update()

    assert contestant.position.coordinates == pytest.approx((2, 0))
    assert contestant.energy == pytest.approx(99)
    assert action.elapsed_time == 1
    assert action.finished is False


def test_contestant_and_random_factory_create_personality_and_skills():
    contestant = Contestant("Ari", "F", Stats(5, 5, 5))
    generated = random_contestant(2)

    assert contestant.personality is not None
    assert contestant.skills is not None
    assert len(generated) == 2
    assert all(item.personality is not None and item.skills is not None for item in generated)


def test_move_reads_position_coordinates():
    contestant = Contestant("Ari", "F", Stats(5, 5, 5), position=Position(3, 4))
    action = Move(contestant, direction=90, speed=1)

    action.update()

    assert contestant.position.coordinates == pytest.approx((3, 5))


def test_contestants_keep_independent_active_action_lists():
    first = Contestant("Ari", "F", Stats(5, 5, 5))
    second = Contestant("Kai", "M", Stats(5, 5, 5))
    action = Defend(first)

    action.update()

    assert first.active_actions == [action]
    assert second.active_actions == []


def test_attack_resolves_damage_and_leaves_active_actions():
    attacker = Contestant("Ari", "F", Stats(5, 5, 5))
    defender = Contestant("Kai", "M", Stats(5, 5, 5))
    action = Attack(attacker, defender)
    action.calculate_damage = lambda: 20

    action.update()
    assert defender.health == 100
    action.update()

    assert defender.health == 80
    assert attacker.energy == 85
    assert action.finished is True
    assert attacker.active_actions == []


def test_attack_damage_is_reduced_by_active_defense():
    attacker = Contestant("Ari", "F", Stats(5, 5, 5))
    defender = Contestant("Kai", "M", Stats(5, 5, 5), armor=20)
    defend = Defend(defender)
    defend.update()
    attack = Attack(attacker, defender)
    attack.calculate_damage = lambda: 20
    attack.update()
    attack.update()

    assert defender.health == 90
