# Plik: Bullet.py
from Parameters.Imports import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage: int, speed: int, position: Tuple[float, float], direction: str) -> None:
        # Inicjalizacja klasy bazowej pygame.sprite.Sprite
        super().__init__()

        # Kierunek lotu pocisku - right, left, up lub down
        self.direction: str = direction

        # Walidacja obrazen - jesli ujemne, ustawiamy wartosc domyslna
        self.damage: int = damage if damage >= 0 else default_damage

        # Walidacja predkosci - jesli ujemna, ustawiamy wartosc domyslna
        self.speed: int = speed if speed >= 0 else default_bullet_speed

        # Dobor sprite'a pocisku w zaleznosci od kierunku lotu
        # Dla gory i dolu obracamy sprite poziomy o 90 stopni
        if direction == "right":
            self.image = BULLET_SPRITES["right"]
        elif direction == "left":
            self.image = BULLET_SPRITES["left"]
        elif direction == "up":
            self.image = pygame.transform.rotate(BULLET_SPRITES["right"], 90)
        elif direction == "down":
            self.image = pygame.transform.rotate(BULLET_SPRITES["left"], 90)

        # Ustawienie prostokata kolizji na podstawie sprite'a i pozycji startowej
        self.rect: pygame.Rect = self.image.get_rect(center=position)

    def update(self) -> None:
        # Przesuwanie pocisku w odpowiednim kierunku co klatke
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # Usuniecie pocisku gdy wyleci poza granice mapy z marginesem out_of_bounds
        if (self.rect.right < -default_out_of_bounds or
            self.rect.left > default_width + default_out_of_bounds or
            self.rect.bottom < -default_out_of_bounds or
            self.rect.top > default_height + default_out_of_bounds):
            self.kill()