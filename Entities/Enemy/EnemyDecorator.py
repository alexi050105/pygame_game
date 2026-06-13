# Plik: EnemyDecorator.py
from Entities.Enemy.Enemy import Enemy


class EnemyDecorator(Enemy):

    def __init__(self, wrapped: Enemy) -> None:
        # Uzycie object.__setattr__ aby uniknac rekurencji w __getattr__
        # podczas ustawiania atrybutu _wrapped
        object.__setattr__(self, "_wrapped", wrapped)

        # Kopiowanie sprite'a i prostokata kolizji z opakowanego przeciwnika
        self.image = wrapped.image
        self.rect = wrapped.rect

    def __getattr__(self, name):
        # Zabezpieczenie przed nieskonczona rekurencja gdy _wrapped nie istnieje
        if name == "_wrapped":
            raise AttributeError("_wrapped not set yet")

        # Delegowanie dostepu do atrybutow do opakowanego przeciwnika
        return getattr(self._wrapped, name)

    def update(self) -> None:
        # Aktualizacja stanu opakowanego przeciwnika
        self._wrapped.update()

        # Synchronizacja sprite'a i prostokata kolizji po aktualizacji
        self.image = self._wrapped.image
        self.rect = self._wrapped.rect

    def move_x(self) -> None:
        # Delegowanie ruchu poziomego do opakowanego przeciwnika
        self._wrapped.move_x()

        # Synchronizacja prostokata kolizji po ruchu
        self.rect = self._wrapped.rect

    def move_y(self) -> None:
        # Delegowanie ruchu pionowego do opakowanego przeciwnika
        self._wrapped.move_y()

        # Synchronizacja prostokata kolizji po ruchu
        self.rect = self._wrapped.rect