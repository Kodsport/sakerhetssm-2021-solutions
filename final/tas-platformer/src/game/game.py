from typing import List
import numpy as np

from .constants import INPUTS
from .utils import Vec2, Rect, boxes_overlap, boxes2_overlap
from .game_board import GameBoard
from .door import Door
from .button import Button
from .boss import Boss
from .level import walls, floors


class Player(Rect):
    HEIGHT = 1.0
    WIDTH = 0.4
    health = 50
    DAMAGE = 20
    can_attack = False
    ATTACK_KOOLDOWN = 200

    def __init__(self, coordinate) -> None:
        super().__init__(coordinate, self.WIDTH, self.HEIGHT)
        self.velocity = Vec2([0, 0])

    def _jump(self):
        if abs(self.velocity.y) < 1e-6:
            self.velocity += Vec2([0, 0.13])

    def _left(self, frame_time):
        self.velocity.x += -0.8 * frame_time

    def _right(self, frame_time):
        self.velocity.x += 0.8 * frame_time

    def enable_attack(self):
        if not self.can_attack:
            self.time_since_last_attack = self.ATTACK_KOOLDOWN
            self.can_attack = True

    def disable_attack(self):
        self.time_since_last_attack = None
        self.can_attack = False

    def attack(self, enemies):
        if not self.can_attack:
            return
        for enemy in enemies:
            if boxes_overlap(self, enemy) and (
                self.time_since_last_attack >= self.ATTACK_KOOLDOWN
            ):
                self.time_since_last_attack = 0
                enemy.health -= self.DAMAGE


class GameState:
    _frame_time = 1.0 / 60.0
    _friction_floor = 0.8
    _friction_wall = 1.0
    _drag = 1.5
    _gravity = 0.3 * _frame_time

    def __init__(self):
        door = Door([19.80, -11.50])
        button = Button([-4.2, -4.40])
        button.add_door(door)
        self.board = GameBoard(floors, walls, [door], [button])

        self.fight_rooms = [Rect([20, -12], width=5, height=7)]
        self.player: Player = Player([-3.0, -3.0])
        self.boss = Boss([24.0, -11.0])
        self.enemies = [self.boss]
        self.entities = [self.player] + self.enemies
        self._moves = [0]

        self.game_running = True
        self.game_won = False

    def game_loop(self, curr_inputs):
        if curr_inputs & INPUTS["B"] and not self._moves[-1] & INPUTS["B"]:
            for button in self.board.buttons:
                button.press(self.player.center)
        if curr_inputs & INPUTS["A"]:
            self.player._left(self._frame_time)
        if curr_inputs & INPUTS["W"] and not self._moves[-1] & INPUTS["W"]:
            self.player._jump()
        if curr_inputs & INPUTS["D"]:
            self.player._right(self._frame_time)
        if curr_inputs & INPUTS["A"]:
            self.player._left(self._frame_time)
        if curr_inputs & INPUTS["SPACE"]:
            self.player.attack(self.enemies)
        if self.player.can_attack:
            self.player.time_since_last_attack += 1
        self.game_mode()
        for entity in self.enemies:
            entity.update(self.player)

        if self.player.health <= 0:
            self.game_running = False

        if self.boss.health <= 0:
            self.game_won = True
            self.game_running = False
        self._move()
        self._moves.append(curr_inputs)

    def game_mode(self):
        if True in [
            boxes_overlap(self.player, fight_room) for fight_room in self.fight_rooms
        ]:
            self.player.enable_attack()
        else:
            self.player.disable_attack()

    def _move(self):
        for entity in self.entities:
            entity.velocity.x -= (
                np.sign(entity.velocity.x) *
                self._drag * entity.velocity.x ** 2
            )
            entity.velocity.y -= self._gravity
            entity.position += entity.velocity

            touching_wall = False
            touching_floor = False
            intersect = boxes2_overlap(self.board.all, entity)
            for i, rect in enumerate(self.board.get_all_rects()):

                r = intersect[i]
                if not r or not rect.blocking:
                    continue
                displacements = [
                    Vec2([rect.right - entity.left, 0]),
                    Vec2([rect.left - entity.right, 0]),
                    Vec2([0, rect.top - entity.bottom]),
                    Vec2([0, rect.bottom - entity.top]),
                ]
                disp_ind = np.linalg.norm(displacements, axis=1).argmin()

                entity.position += displacements[disp_ind]
                if disp_ind == 0 or disp_ind == 1:
                    entity.velocity.x = 0
                    touching_wall = True
                else:
                    entity.velocity.y = 0
                    touching_floor = True
                intersect = boxes2_overlap(self.board.all, entity)

            if touching_wall:
                entity.velocity.y *= self._friction_wall
            if touching_floor:
                entity.velocity.x *= self._friction_floor

    def elapsed_time(self):
        return self._frame_time * len(self._moves)
