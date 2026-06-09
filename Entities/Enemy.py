
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

        super().__init__(name, HP, starting_position, damage, speed)

        self.image: pygame.Surface = ENEMY_SPRITES["right"]
        self.rect: pygame.Rect = self.image.get_rect(center = starting_position)
        self.player: pygame.sprite.Sprite = player

    def update(self) -> None:
        self.image = ENEMY_SPRITES["right"] if self.rect.centerx <= self.player.rect.centerx else ENEMY_SPRITES["left"]

    def move_x(self) -> None:
        if self.rect.centerx < self.player.rect.centerx:
            self.rect.centerx += self.speed
        elif self.rect.centerx > self.player.rect.centerx:
            self.rect.centerx -= self.speed

    def move_y(self) -> None:
        if self.rect.centery < self.player.rect.centery:
            self.rect.centery += self.speed
        elif self.rect.centery > self.player.rect.centery:
            self.rect.centery -= self.speed