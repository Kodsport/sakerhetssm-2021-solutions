from .utils import Vec2
from typing import List, Type
from .door import Door
import numpy as np


class Button:
    doors: List[Door] = []

    def __init__(self, coordinates):
        self.position: Vec2 = Vec2(coordinates)
        self.distance = 1
        self.is_pressed = False

    def allowed(self, position: Vec2) -> bool:
        distance = np.linalg.norm(self.position - position)
        if distance <= self.distance:
            return True

    def add_door(self, door: Door):
        self.doors.append(door)

    def toggle(self):
        self.is_pressed = not self.is_pressed

    def press(self, position: Vec2):
        if self.allowed(position):
            self.toggle()
            for door in self.doors:
                door.toggle()
