# Plik: Bullet.py
from Parameters.Imports import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage: int, speed: int, position: Tuple[float, float], facing_right: bool) -> None:
        super().__init__()
        self.facing_right: bool = facing_right
        self.image: pygame.Surface = BULLET_SPRITES["right"] if facing_right else BULLET_SPRITES["left"]
        self.rect: pygame.Rect = self.image.get_rect(center=position)
        self.damage: int = damage if damage >= 0 else default_damage
        self.speed: int = speed if speed >= 0 else default_bullet_speed

    def update(self) -> None:
        if self.facing_right:
            self.rect.right += self.speed
        else:
            self.rect.left -= self.speed

        if self.rect.right < 0 or self.rect.left > default_width:
            self.kill()