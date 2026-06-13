# Plik: FastEnemy.py
from Entities.Enemy.EnemyDecorator import EnemyDecorator
from Parameters.Imports import *


class FastEnemy(EnemyDecorator):

    def __init__(self, wrapped, multiplier: float = default_fast_enemy_multiplier) -> None:
        # Inicjalizacja dekoratora z opakowanym przeciwnikiem
        super().__init__(wrapped)

        # Mnoznik predkosci - domyslnie pobierany z parametrow domyslnych
        self.multiplier = multiplier

    def update(self) -> None:
        # Aktualizacja stanu opakowanego przeciwnika
        self._wrapped.update()

        # Dobor sprite'a w zaleznosci od kierunku patrzenia na gracza
        self.image = FAST_ENEMY_SPRITES["right"] if self.rect.centerx \
                <= self.player.rect.centerx else FAST_ENEMY_SPRITES["left"]

        # Synchronizacja prostokata kolizji z opakowanym przeciwnikiem
        self.rect = self._wrapped.rect

    def move_x(self) -> None:
        # Zapamietanie oryginalnej predkosci przed zwiekszeniem
        original_speed = self._wrapped.speed

        # Tymczasowe zwiekszenie predkosci o mnoznik
        self._wrapped.speed = int(original_speed * self.multiplier)
        self._wrapped.move_x()

        # Przywrocenie oryginalnej predkosci po wykonaniu ruchu
        self._wrapped.speed = original_speed

        # Synchronizacja prostokata kolizji z opakowanym przeciwnikiem
        self.rect = self._wrapped.rect

    def move_y(self) -> None:
        # Zapamietanie oryginalnej predkosci przed zwiekszeniem
        original_speed = self._wrapped.speed

        # Tymczasowe zwiekszenie predkosci o mnoznik
        self._wrapped.speed = int(original_speed * self.multiplier)
        self._wrapped.move_y()

        # Przywrocenie oryginalnej predkosci po wykonaniu ruchu
        self._wrapped.speed = original_speed

        # Synchronizacja prostokata kolizji z opakowanym przeciwnikiem
        self.rect = self._wrapped.rect