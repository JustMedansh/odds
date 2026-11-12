import pytest
from src.actions.encounter import Encounter
from src.contestants.contestant import Contestant

@pytest.fixture
def contestants():
    return [object(), object(), object()]

def test_init(contestants):
    a, b, c = contestants
    encounter = Encounter([a, b])

    assert encounter.active == True
    assert encounter.contestants == [a, b]

def test_add(contestants):
    a, b, c = contestants
    encounter = Encounter([a, b])

    encounter.add_contestant(c)
    assert encounter.contains(c)
    assert c in encounter.contestants 

def test_contains(contestants):
    a, b, c = contestants
    encounter = Encounter([a, b])

    assert encounter.contains(a) is True
    assert encounter.contains(c) is False


def test_no_duplicates(contestants):
    a, b, c = contestants
    encounter = Encounter([a, b])

    encounter.add_contestant(a)

    assert encounter.contestants.count(a) == 1