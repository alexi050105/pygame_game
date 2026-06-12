# Plik: Person.py
from Parameters.Imports import *


class Person(pygame.sprite.Sprite, ABC):
    def __init__(self, name: str, HP: int, starting_position: Tuple[float, float], damage: int, speed: int) -> None:
        # Inicjalizacja klasy bazowej pygame.sprite.Sprite
        super().__init__()

        # Przypisanie nazwy postaci
        self.name: str = name

        # Walidacja HP - jesli podano nieprawidlowa wartosc, ustawiamy domyslna
        self.HP: int = HP if HP > 0 else default_HP

        # Walidacja predkosci - predkosc nie moze byc ujemna
        self.speed: int = speed if speed >= 0 else default_player_speed

        # Walidacja obrazen - obrazenia nie moga byc ujemne
        self.damage: int = damage if damage >= 0 else default_damage

        # Walidacja pozycji startowej - jesli pozycja jest poza mapa, ustawiamy srodek
        start_x = default_width / 2 if (starting_position[0] < -default_out_of_bounds or starting_position[
            0] > default_width + default_out_of_bounds) else starting_position[0]
        start_y = default_height / 2 if (starting_position[1] < -default_out_of_bounds or starting_position[
            1] > default_height + default_out_of_bounds) else starting_position[1]
        self.starting_position: Tuple[float, float] = (start_x, start_y)

        # Domyslnie postac jest zwrocona w prawo
        self.facing_right: bool = True

        # Obrazek i prostokat kolizji sa ustawiane przez klasy potomne
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

    def handle_movement_keys(self) -> None:
        # Pobieranie aktualnie wcisnietych klawiszy
        keys = pygame.key.get_pressed()

        # Ruch w gore - ograniczenie do gornej krawedzi mapy
        if keys[pygame.K_w]:
            self.rect.top = max(0, self.rect.top - self.speed)
        # Ruch w dol - ograniczenie do dolnej krawedzi mapy
        elif keys[pygame.K_s]:
            self.rect.bottom = min(default_height, self.rect.bottom + self.speed)

        # Ruch w lewo - ograniczenie do lewej krawedzi mapy, zmiana kierunku sprite'a
        if keys[pygame.K_a]:
            self.rect.left = max(0, self.rect.left - self.speed)
            self.facing_right = False
        # Ruch w prawo - ograniczenie do prawej krawedzi mapy, zmiana kierunku sprite'a
        elif keys[pygame.K_d]:
            self.rect.right = min(default_width, self.rect.right + self.speed)
            self.facing_right = True