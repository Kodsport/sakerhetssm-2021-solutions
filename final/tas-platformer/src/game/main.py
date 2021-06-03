from typing import List
import numpy as np

from constants import INPUTS


class Vec2(np.ndarray):
    def __new__(_, input_array=(np.nan, np.nan)):
        obj = np.asarray(input_array, dtype=np.float64).view(Vec2)
        return obj

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @x.setter
    def x(self, value):
        self[0] = value

    @y.setter
    def y(self, value):
        self[1] = value


class Player:
    PLAYER_HEIGHT = 1.0
    PLAYER_WIDTH = 0.2

    def __init__(self, coordinates) -> None:
        self.position = Vec2(coordinates)

    @property
    def head(self) -> Vec2:
        return Vec2([0, self.PLAYER_HEIGHT])+self.position

    @property
    def feet(self) -> Vec2:
        return self.position + Vec2([0, 0])

    @property
    def left_side(self) -> Vec2:
        return Vec2([-self.PLAYER_WIDTH, 0])+self.position

    @property
    def right_side(self) -> Vec2:
        return Vec2([self.PLAYER_WIDTH, 0])+self.position


class Floor:

    def __init__(self, coordinates, width=1.5) -> None:
        self.position = Vec2(coordinates)
        self.FLOOR_WIDTH = width

    def intersect(self, player: Player):
        if player.position.x+player.PLAYER_WIDTH > self.position.x and player.position.x-player.PLAYER_WIDTH < self.position.x+self.FLOOR_WIDTH:
            if player.position.y < self.position.y and player.head.y > self.position.y:
                return self.position.y
        return None


class Wall:

    def __init__(self, coordinates, height=5) -> None:
        self.position = Vec2(coordinates)
        self.WALL_HEIGHT = height

    def intersect(self, player: Player):
        if self.position.y < player.head.y and self.position.y+self.WALL_HEIGHT > player.feet.y:
            if self.position.x > player.left_side.x and self.position.x < player.right_side.x:
                return self.position.x
        return None


class GameBoard:
    floors: List[Floor] = [Floor([0, -1]), Floor([1, -2.5]), Floor([-1, -3])] + [
        Floor([i*1.5, -4]) for i in range(-5, 6)]
    walls: List[Wall] = [Wall([-1, -2])]

    def collision(self, player):
        x, y = None, None
        for wall in self.walls:
            res = wall.intersect(player)
            if res != None:
                x = res
        for floor in self.floors:
            res = floor.intersect(player)
            if res != None:
                y = res
        return x, y


class GameState:
    _moves = [0]
    _frame_time = 1./60.
    player: Player = Player([1.5, 0])
    _velocity = Vec2([0, 0])
    board = GameBoard()
    _friction_floor = 0.6
    _friction_wall = 0.6
    _touching_floor = True
    _touching_wall = False
    _gravity = 0.3*_frame_time
    _is_sprinting = False

    def game_loop(self, curr_inputs):
        if curr_inputs & INPUTS["A"]:
            self._left()
        if curr_inputs & INPUTS["D"]:
            self._jump()
        if curr_inputs & INPUTS["W"]:
            self._right()
        self._move()
        self._moves.append(curr_inputs)

    def _jump(self):
        if self._touching_floor:
            self._velocity += Vec2([0, 0.12])

    def _left(self):
        self._velocity.x = (-2.5 if self._is_sprinting else -
                            1.5)*self._frame_time

    def _right(self):
        self._velocity.x = (
            2.5 if self._is_sprinting else 1.5)*self._frame_time

    def _move(self):
        self.player.position += self._velocity
        x, y = self.board.collision(self.player)
        if x:
            self._touching_wall = True
            self.player.position.x = x - (self._velocity.x /
                                          abs(self._velocity.x))*self.player.PLAYER_WIDTH
            self._velocity.x = 0
        else:
            self._touching_wall = False

        if y:
            if self._velocity.y > 0:
                self.player.position.y = y-self.player.PLAYER_HEIGHT
                self._touching_floor = False
            else:
                self._touching_floor = True
                self.player.position.y = y
            self._velocity.y = 0
        else:
            self._touching_floor = False
        if self._touching_wall:
            self._velocity.y *= self._friction_wall
        if self._touching_floor:
            self._velocity.x *= self._friction_floor
        self._velocity.y -= self._gravity

    def elapsed_time(self):
        return self._frame_time*len(self._moves)
