# Plik: Enemy.py
from Parameters.Imports import *
from Entities.Person import Person


class Enemy(Person):
    def __init__(self,
                 name: str,
                 HP: int,
                 starting_position: Tuple[float, float],
                 damage: int,
                 speed: int,
                 player: pygame.sprite.Sprite) -> None:

        # Inicjalizacja klasy bazowej Person
        super().__init__(name, HP, starting_position, damage, speed)

        # Ustawienie domyslnego sprite'a przeciwnika skierowanego w prawo
        self.image: pygame.Surface = BASE_ENEMY_SPRITES["right"]

        # Ustawienie prostokata kolizji na podstawie sprite'a i pozycji startowej
        self.rect: pygame.Rect = self.image.get_rect(center=starting_position)

        # Referencja do gracza - przeciwnik bedzie sie w jego kierunku poruszac
        self.player: pygame.sprite.Sprite = player

    def update(self) -> None:
        # Aktualizacja kierunku patrzenia na podstawie pozycji gracza
        self.facing_right = self.rect.centerx <= self.player.rect.centerx

        # Dobor sprite'a w zaleznosci od kierunku patrzenia
        self.image = BASE_ENEMY_SPRITES["right"] if self.facing_right else BASE_ENEMY_SPRITES["left"]

    def move_x(self) -> None:
        # Poruszanie sie w kierunku gracza wzgledem osi X
        if self.rect.centerx < self.player.rect.centerx:
            self.rect.centerx += self.speed
        elif self.rect.centerx > self.player.rect.centerx:
            self.rect.centerx -= self.speed

    def move_y(self) -> None:
        # Poruszanie sie w kierunku gracza wzgledem osi Y
        if self.rect.centery < self.player.rect.centery:
            self.rect.centery += self.speed
        elif self.rect.centery > self.player.rect.centery:
            self.rect.centery -= self.speed