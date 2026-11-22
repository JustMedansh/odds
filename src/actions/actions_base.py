from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.contestants import Contestant

class Action:
    """Base class for contestant actions."""
    def __init__(self, contestant: Contestant):
        self.contestant = contestant
        self.elapsed_time = 0
        self.duration = 1

        self.interrupted = False
        self.finished = False

    def start(self):
        """Called once when the action begins."""
        pass

    def on_tick(self):
        """Called every simulation tick"""
        pass

    def update(self):
        """Called every simulation tick."""
        self.elapsed_time += 1
        self.on_tick()

        if self.interrupted or (self.duration is not None and self.elapsed_time >= self.duration):
            self.resolve()
            self.finished = True

    def interrupt(self):
        """End the current Action with no benefit"""
        if self.finished:
            return False

        self.on_interrupt()

        self.interrupted = True
        self.finished = True
        return True

    def resolve(self):
        """Apply the action's consequences."""
        raise NotImplementedError

    def on_interrupt(self):
        """Handle consequences of interruption."""
        pass
