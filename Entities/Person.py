# Plik: Person.py
from Parameters.Imports import *


class Person(pygame.sprite.Sprite, ABC):
    def __init__(self, name: str, HP: int, starting_position: Tuple[float, float], damage: int, speed: int) -> None:
        super().__init__()
        self.name: str = name
        self.HP: int = HP if HP > 0 else default_HP
        self.speed: int = speed if speed >= 0 else default_player_speed
        self.damage: int = damage if damage >= 0 else default_damage

        # Walidacja pozycji startowej
        start_x = default_width / 2 if (starting_position[0] < -default_out_of_bounds or starting_position[
            0] > default_width + default_out_of_bounds) else starting_position[0]
        start_y = default_height / 2 if (starting_position[1] < -default_out_of_bounds or starting_position[
            1] > default_height + default_out_of_bounds) else starting_position[1]
        self.starting_position: Tuple[float, float] = (start_x, start_y)

        self.facing_right: bool = True
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

    def handle_movement_keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.top = max(0, self.rect.top - self.speed)
        elif keys[pygame.K_s]:
            self.rect.bottom = min(default_height, self.rect.bottom + self.speed)
        if keys[pygame.K_a]:
            self.rect.left = max(0, self.rect.left - self.speed)
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.rect.right = min(default_width, self.rect.right + self.speed)
            self.facing_right = True