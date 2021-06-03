from .utils import Vec2, Rect
from .door import Door
from .button import Button
import numpy as np


class Floor(Rect):
    def __init__(self, coordinates, width=1.5) -> None:
        super().__init__(coordinates, width, 0)


class Wall(Rect):
    def __init__(self, coordinates, height=1.5) -> None:
        super().__init__(coordinates, 0, height)


class GameBoard:
    def __init__(self, floors, walls, doors, buttons):
        self.floors = floors
        self.walls = walls
        self.doors = doors
        self.buttons = buttons
        self.all = np.array([i.np_arr for i in floors] +
                            [i.np_arr for i in walls]+[i.np_arr for i in doors])

    def get_all_rects(self):
        return self.floors + self.walls + [d for d in self.doors if not d.open]
