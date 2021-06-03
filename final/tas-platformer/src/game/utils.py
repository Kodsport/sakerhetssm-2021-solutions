from typing import List
import numpy as np


class Vec2(np.ndarray):
    def __new__(_, input_array):
        obj = np.asarray(input_array, dtype=np.float64).view(Vec2)
        return obj

    @property
    def x(self) -> float:
        return self[0]

    @property
    def y(self) -> float:
        return self[1]

    @x.setter
    def x(self, value):
        self[0] = value

    @y.setter
    def y(self, value):
        self[1] = value


class Rect:
    def __init__(
        self,
        coordinates: List[float],
        width: float,
        height: float,
        blocking: bool = True,
    ) -> None:
        self.position = Vec2(coordinates)
        self.width: float = width
        self.height: float = height
        self.blocking: bool = blocking

    @property
    def top(self) -> float:
        return self.position.y + self.height

    @property
    def bottom(self) -> float:
        return self.position.y

    @property
    def left(self) -> float:
        return self.position.x

    @property
    def right(self) -> float:
        return self.position.x + self.width

    @property
    def center(self) -> float:
        return self.position + [self.width / 2, self.height / 2]

    @property
    def np_arr(self):
        return [self.right, self.left, self.top, self.bottom]


def boxes_overlap(box1: Rect, box2: Rect) -> bool:
    if not (box1.blocking and box2.blocking):
        return False
    return box1.right > box2.left and box2.right > box1.left and box1.top > box2.bottom and box2.top > box1.bottom


def boxes2_overlap(box1, box2: Rect):
    return np.logical_and((box1[:, 0] > box2.left), np.logical_and((box2.right > box1[:, 1]), np.logical_and((box1[:, 2] > box2.bottom), (box2.top > box1[:, 3]))))
