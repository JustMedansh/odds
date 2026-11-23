from ..actions_base import Action

class Rest(Action):
    """Default action when no action is taking place"""
    def __init__(self, contestant):
        super().__init__(contestant)
        self.duration = None

    def on_interrupt(self):
        self.resolve()

    def resolve(self):
        self.contestant.heal(self.elapsed_time * 0.5)
        self.contestant.add_energy(self.elapsed_time)