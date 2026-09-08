from enum import Enum


class GhostStatus(Enum):
    CHASE = "chase"
    EDIBLE = "edible"
    EATEN = "eaten"


class GhostMovement:
    pass


class Ghost:
    position: tuple[int, int]
    state: GhostStatus
    spawn_pos: tuple[int, int]

    def __init__(self, pos: tuple[int, int]) -> None:
        self.spawn_pos = pos
        self.pos = self.spawn_pos
        self.state = GhostStatus.CHASE

    def move(self) -> None:
        pass

    def become_edible(self) -> None:
        self.state = GhostStatus.EDIBLE

    def get_eaten(self) -> None:
        self.state = GhostStatus.EATEN

    def respawn(self) -> None:
        self.state = GhostStatus.CHASE
