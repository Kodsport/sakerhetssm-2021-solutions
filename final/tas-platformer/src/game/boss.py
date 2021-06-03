from typing import List
import numpy as np
from .utils import Vec2, Rect, boxes_overlap

# from game import Player


class Boss(Rect):
    HEIGHT = 3
    WIDTH = 1
    SPEED = 0.03
    health = 100
    DAMAGE = 2
    ATTACK_KOOLDOWN = 10
    _time_since_last_attack = 0

    def __init__(self, coordinate) -> None:
        super().__init__(coordinate, self.WIDTH, self.HEIGHT)
        self.velocity = Vec2([0, 0])

    def update(self, player):
        if player.can_attack:
            self.attack(player)
            self.move(player)

    def attack(self, player):
        if boxes_overlap(self, player) and (
            self._time_since_last_attack >= self.ATTACK_KOOLDOWN
        ):
            self._time_since_last_attack = 0
            player.health -= self.DAMAGE
        self._time_since_last_attack += 1

    def move(self, player):
        # self.position = player.position - self.position
        if not boxes_overlap(self, player):
            self.position.x += self.SPEED * \
                np.sign(player.position.x - self.position.x)
