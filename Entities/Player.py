# Plik: Player.py
from Parameters.Imports import *
from Entities.Person import Person
from Entities.Bullet import Bullet

class Player(Person):
    def __init__(self, name: str, HP: int, starting_position: Tuple[float, float], damage: int, speed: int, bullets_group: pygame.sprite.Group) -> None:
        super().__init__(name, HP, starting_position, damage, speed)
        self.image: pygame.Surface = PLAYER_SPRITES["right"]

        start_x = default_width / 2 if (starting_position[0] < -default_out_of_bounds or starting_position[
            0] > default_width + default_out_of_bounds) else starting_position[0]
        start_y = default_height / 2 if (starting_position[1] < -default_out_of_bounds or starting_position[
            1] > default_height + default_out_of_bounds) else starting_position[1]

        self.starting_position = (start_x, start_y)

        self.rect: pygame.Rect = self.image.get_rect(center=self.starting_position)
        self.game_bullets: pygame.sprite.Group = bullets_group
        self.cooldown: int = 0
        self.facing_vertical: str = ""

    def update(self) -> None:
        self.handle_movement_keys()
        self.image = PLAYER_SPRITES["right"] if self.facing_right else PLAYER_SPRITES["left"]
        if self.cooldown > 0:
            self.cooldown -= 1
        keys = pygame.key.get_pressed()
        if self.cooldown == 0:
            if keys[pygame.K_RIGHT]:
                self.facing_right = True
                self.shoot("right")
            elif keys[pygame.K_LEFT]:
                self.facing_right = False
                self.shoot("left")
            elif keys[pygame.K_UP]:
                self.shoot("up")
            elif keys[pygame.K_DOWN]:
                self.shoot("down")

    def shoot(self, direction: str) -> None:
        if direction == "right":
            pos: Tuple[float, float] = self.rect.midright
        elif direction == "left":
            pos: Tuple[float, float] = self.rect.midleft
        elif direction == "up":
            pos: Tuple[float, float] = self.rect.midtop
        elif direction == "down":
            pos: Tuple[float, float] = self.rect.midbottom

        new_bullet: Bullet = Bullet(self.damage, default_bullet_speed, pos, direction)
        self.game_bullets.add(new_bullet)
        self.cooldown = default_bullet_cooldown

        import Parameters.Imports as assets
        assets.SOUNDS["shoot"].play()