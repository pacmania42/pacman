from random import randint

from src.adapter import Adapter


class Level:
    rank: int
    width: int
    height: int
    seed: int
    generator: Adapter

    def __init__(self, rank: int, width: int, height: int):
        self.rank = rank
        self.width = width
        self.height = height
        self.seed = randint(-1000, 1000) if rank > 0 else 42

        self.generator = Adapter(self.width, self.height, self.seed)
