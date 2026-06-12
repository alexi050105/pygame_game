# Plik: Player.py
from Parameters.Imports import *
from Entities.Person import Person
from Entities.Bullet import Bullet


class Player(Person):
    def __init__(self, name: str, HP: int, starting_position: Tuple[float, float], damage: int, speed: int, bullets_group: pygame.sprite.Group) -> None:
        # Inicjalizacja klasy bazowej Person
        super().__init__(name, HP, starting_position, damage, speed)

        # Ustawienie domyslnego sprite'a gracza skierowanego w prawo
        self.image: pygame.Surface = PLAYER_SPRITES["right"]

        # Walidacja pozycji startowej - jesli poza mapa, ustawiamy srodek ekranu
        start_x = default_width / 2 if (starting_position[0] < -default_out_of_bounds or starting_position[
            0] > default_width + default_out_of_bounds) else starting_position[0]
        start_y = default_height / 2 if (starting_position[1] < -default_out_of_bounds or starting_position[
            1] > default_height + default_out_of_bounds) else starting_position[1]
        self.starting_position = (start_x, start_y)

        # Ustawienie prostokata kolizji na podstawie sprite'a i pozycji startowej
        self.rect: pygame.Rect = self.image.get_rect(center=self.starting_position)

        # Referencja do grupy pociskow przekazana z zewnatrz
        self.game_bullets: pygame.sprite.Group = bullets_group

        # Cooldown strzalu - zapobiega strzelaniu zbyt szybko
        self.cooldown: int = 0

        # Kierunek pionowy strzalu (up/down) - domyslnie pusty
        self.facing_vertical: str = ""

    def update(self) -> None:
        # Obsluga ruchu gracza za pomoca klawiszy WASD
        self.handle_movement_keys()

        # Aktualizacja sprite'a w zaleznosci od kierunku patrzenia
        self.image = PLAYER_SPRITES["right"] if self.facing_right else PLAYER_SPRITES["left"]

        # Zmniejszanie cooldownu co klatke az do zera
        if self.cooldown > 0:
            self.cooldown -= 1

        # Obsluga strzalu strzalkami - tylko gdy cooldown wynosi 0
        keys = pygame.key.get_pressed()
        if self.cooldown == 0:
            if keys[pygame.K_RIGHT]:
                # Strzal w prawo i aktualizacja kierunku patrzenia
                self.facing_right = True
                self.shoot("right")
            elif keys[pygame.K_LEFT]:
                # Strzal w lewo i aktualizacja kierunku patrzenia
                self.facing_right = False
                self.shoot("left")
            elif keys[pygame.K_UP]:
                # Strzal w gore
                self.shoot("up")
            elif keys[pygame.K_DOWN]:
                # Strzal w dol
                self.shoot("down")

    def shoot(self, direction: str) -> None:
        # Wyznaczenie pozycji startowej pocisku w zaleznosci od kierunku strzalu
        if direction == "right":
            pos: Tuple[float, float] = self.rect.midright
        elif direction == "left":
            pos: Tuple[float, float] = self.rect.midleft
        elif direction == "up":
            pos: Tuple[float, float] = self.rect.midtop
        elif direction == "down":
            pos: Tuple[float, float] = self.rect.midbottom

        # Tworzenie nowego pocisku i dodanie go do grupy pociskow
        new_bullet: Bullet = Bullet(self.damage, default_bullet_speed, pos, direction)
        self.game_bullets.add(new_bullet)

        # Ustawienie cooldownu po oddaniu strzalu
        self.cooldown = default_bullet_cooldown

        # Odtworzenie dzwieku strzalu
        import Parameters.Imports as assets
        assets.SOUNDS["shoot"].play()