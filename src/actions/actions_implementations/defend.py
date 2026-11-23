from __future__ import annotations
from typing import TYPE_CHECKING
from ..actions_base import Action

if TYPE_CHECKING:
    from src.contestants import Contestant

class Defend(Action):
    """Defend against oncoming damage of any type"""
    def __init__(self, contestant: Contestant):
        super().__init__(contestant)
        self.duration = None

    def on_tick(self):
        self.contestant.reduce_energy(0.5)

    def resolve(self):
        pass
