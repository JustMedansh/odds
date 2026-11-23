from src.contestants import Contestant

def resolve_fighting(damage: float, attacker: Contestant, defender: Contestant):
    """Resolve damage taken between two contestants"""
    from src.actions.actions_implementations.attack import Attack
    from src.actions.actions_implementations.defend import Defend

    if not any(isinstance(action, Attack) for action in attacker.active_actions):
        raise ValueError("Function must only be called during an active Attack")

    damage_multiplier = 1.0

    if any(isinstance(action, Defend) for action in defender.active_actions):
        damage_multiplier = max(0, 1 - (defender.armor / 40))

    defender.take_damage(max(0, damage) * damage_multiplier)
