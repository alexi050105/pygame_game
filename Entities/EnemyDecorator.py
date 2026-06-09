from Parameters.Imports import *
from Entities.Enemy import Enemy

class EnemyDecorator(Enemy):

    def __init__(self, wrapped: Enemy) -> None:

        object.__setattr__(self, "_wrapped", wrapped)

        self.image = wrapped.image
        self.rect = wrapped.rect


    def __getattr__(self, name):

        if name == "_wrapped":
            raise AttributeError("_wrapped not set yet")

        return getattr(self._wrapped, name)


    def update(self) -> None:
        self._wrapped.update()
        self.image = self._wrapped.image
        self.rect = self._wrapped.rect

    def move_x(self) -> None:
        self._wrapped.move_x()

    def move_y(self) -> None:
        self._wrapped.move_y()






