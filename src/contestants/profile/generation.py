from enum import Enum, auto
import random

class GenerationBias(Enum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()

def generate_value(minimum: int, maximum: int, bias: GenerationBias) -> float:
    values = range(minimum, maximum + 1)
    weights = generate_weights(minimum, maximum, bias)

    return random.choices(values, weights, k=1)[0]

def generate_weights(minimum: int, maximum: int, bias: GenerationBias) -> float:
    count = maximum - minimum + 1

    if bias == GenerationBias.NORMAL:
        midpoint = (count - 1) / 2
        weights = [count - abs(i - midpoint) for i in range(count)]

    elif bias == GenerationBias.LOW:
        weights = list(range(count, 0, -1))

    elif bias == GenerationBias.HIGH:
        weights = list(range(1, count + 1))

    return weights

BIAS_TABLE = {
        GenerationBias.LOW: (1, 5),
        GenerationBias.NORMAL: (1, 10),
        GenerationBias.HIGH: (5, 10)
    }
