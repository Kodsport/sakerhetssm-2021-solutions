from .utils import Rect


class Door(Rect):
    def __init__(self, coordinates, height=1.5, open: bool = False) -> None:
        super().__init__(coordinates, 0, height)
        self.open = open

    def toggle(self):
        self.open = not self.open
        self.blocking = not self.blocking
