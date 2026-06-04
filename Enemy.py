from Person import *

import pygame

ENEMY_SPRITES = {}

enemy_sprite_left = "graphics/enemy_left.png"
enemy_sprite_right = "graphics/enemy_right.png"

ENEMY_SPRITES = {}
def load_enemy_images():
    global ENEMY_SPRITES
    raw_left = pygame.image.load(enemy_sprite_left).convert_alpha()
    raw_right = pygame.image.load(enemy_sprite_right).convert_alpha()

    default_size = (50, 50)

    # Tutaj możesz też dodać skalowanie transform.scale(), jeśli przeciwnicy są za duży!
    ENEMY_SPRITES["left"] = pygame.transform.smoothscale(raw_left, default_size)
    ENEMY_SPRITES["right"] = pygame.transform.smoothscale(raw_right, default_size)

class Enemy(Person):

    def __init__(self, name,
                 HP,
                 starting_position,
                 damage,
                 speed,
                 player):

        super().__init__(name, HP, starting_position, damage, speed)

        self.facing_right = True

        self.image = ENEMY_SPRITES["right"]
        self.rect = self.image.get_rect(center = starting_position)

        self.player = player


    def update(self):
        pass


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


