# Entities/HealthPack.py
import Parameters.Imports as assets
from Parameters.Imports import *


class HealthPack(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int], heal_amount: int) -> None:
        # Inicjalizacja klasy bazowej pygame.sprite.Sprite
        super().__init__()

        # Ustawienie sprite'a apteczki z globalnego slownika grafik
        self.image = assets.HEALTHPACK_SPRITE

        # Ustawienie prostokata kolizji na podstawie sprite'a i podanej pozycji
        self.rect = self.image.get_rect(center=position)

        # Ilosc HP ktora apteczka przywraca po zebraniu
        self.heal_amount = heal_amount

        # Czas zycia apteczki w klatkach - po jego uplywie apteczka znika z mapy
        self.lifetime: int = default_healthpack_lifetime

    def update(self) -> None:
        # Zmniejszanie czasu zycia apteczki co klatke
        self.lifetime -= 1

        # Usuniecie apteczki z gry gdy czas zycia dobiegnie konca
        if self.lifetime <= 0:
            self.kill()