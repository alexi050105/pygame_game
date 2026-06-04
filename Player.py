from Person import *

from DefaultParameters import *

from Bullet import *

player_sprite_left = "graphics/player_left.png"
player_sprite_right = "graphics/player_right.png"

PLAYER_SPRITES = {}
def load_player_images():
    global PLAYER_SPRITES
    # Tutaj możesz też dodać skalowanie transform.scale(), jeśli przeciwnicy są za duży!
    raw_left = pygame.image.load(player_sprite_left).convert_alpha()
    raw_right = pygame.image.load(player_sprite_right).convert_alpha()

    default_size = (50, 50)

    PLAYER_SPRITES["left"] = pygame.transform.smoothscale(raw_left, default_size)
    PLAYER_SPRITES["right"] = pygame.transform.smoothscale(raw_right, default_size)

class Player(Person):

    def __init__(self,
                 name,
                 HP,
                 starting_position,
                 damage,
                 speed,
                 bullets_group):  # <-- DODANE w argumentach

        super().__init__(name, HP, starting_position, damage, speed)

        self.image = PLAYER_SPRITES["right"]
        self.facing_right = True
        self.rect = self.image.get_rect(center=self.starting_position)

        # TUTAJ: Przypisujemy globalną grupę zamiast tworzyć własną, pustą
        self.game_bullets = bullets_group
        self.cooldown = 0

    def __change_sprite_dir(self):

        if self.facing_right:
            self.image = PLAYER_SPRITES["right"]
        else:
            self.image = PLAYER_SPRITES["left"]

    def update(self):
        super().update()

        keys = pygame.key.get_pressed()

        self.__change_sprite_dir()

        if self.cooldown > 0:
            self.cooldown -= 1

        # TUTAJ: Strzelaj tylko wtedy, gdy cooldown minął!
        if keys[pygame.K_SPACE] and self.cooldown == 0:
            self.shoot()

    def shoot(self):

        if self.facing_right: pos = self.rect.midright
        else:                 pos = self.rect.midleft

        new_bullet = Bullet(self.damage,
                            default_bullet_speed,
                            pos,
                            self.facing_right)

        # TUTAJ: Dodajemy pocisk do grupy gry
        self.game_bullets.add(new_bullet)

        # Zmieniamy cooldown na wartość ze zmiennych domyślnych
        self.cooldown = default_bullet_cooldown