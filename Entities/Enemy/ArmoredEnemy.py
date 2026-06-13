# Plik: ArmoredEnemy.py
from Entities.Enemy.EnemyDecorator import EnemyDecorator
from Parameters.Imports import *


class ArmoredEnemy(EnemyDecorator):

    def __init__(self, wrapped) -> None:
        # Inicjalizacja dekoratora z opakowanym przeciwnikiem
        super().__init__(wrapped)

        # Liczba trafien potrzebnych do zabicia opancerzonego przeciwnika
        self.hits_remaining: int = default_armored_enemy_hits

    def update(self) -> None:
        # Aktualizacja stanu opakowanego przeciwnika
        self._wrapped.update()

        # Dobor sprite'a w zaleznosci od kierunku patrzenia na gracza
        self.image = ARMORED_ENEMY_SPRITES["right"] if self.rect.centerx \
                <= self.player.rect.centerx else ARMORED_ENEMY_SPRITES["left"]

        # Synchronizacja prostokata kolizji z opakowanym przeciwnikiem
        self.rect = self._wrapped.rect

    def take_hit(self) -> bool:
        # Zmniejszenie liczby pozostalych trafien po otrzymaniu obrazenia
        self.hits_remaining -= 1

        # Jesli wszystkie trafienia zostaly zadane - przeciwnik ginie
        if self.hits_remaining <= 0:
            return True

        # Wizualna informacja o trafieniu - efekt uszkodzenia sprite'a
        self.image = pygame.transform.laplacian(self._wrapped.image)

        # Przeciwnik jeszcze zyje
        return False