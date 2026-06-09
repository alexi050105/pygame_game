# Plik: Player.py
from Parameters.Imports import *
from Entities.Person import Person
from Entities.Bullet import Bullet

class Player(Person):
    def __init__(self, name: str, HP: int, starting_position: Tuple[float, float], damage: int, speed: int, bullets_group: pygame.sprite.Group) -> None:
        super().__init__(name, HP, starting_position, damage, speed)
        self.image: pygame.Surface = PLAYER_SPRITES["right"]
        self.rect: pygame.Rect = self.image.get_rect(center=self.starting_position)
        self.game_bullets: pygame.sprite.Group = bullets_group
        self.cooldown: int = 0

    def update(self) -> None:
        self.handle_movement_keys()
        self.image = PLAYER_SPRITES["right"] if self.facing_right else PLAYER_SPRITES["left"]

        if self.cooldown > 0:
            self.cooldown -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            self.shoot()

    def shoot(self) -> None:
        pos = self.rect.midright if self.facing_right else self.rect.midleft
        new_bullet = Bullet(self.damage, default_bullet_speed, pos, self.facing_right)
        self.game_bullets.add(new_bullet)
        self.cooldown = default_bullet_cooldown