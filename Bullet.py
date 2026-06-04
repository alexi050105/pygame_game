import pygame

from DefaultParameters import *

bullet_img_left = "graphics/bullet_left.png"
bullet_img_right = "graphics/bullet_right.png"

BULLET_SPRITES = {}

def load_bullet_images():
    global BULLET_SPRITES

    raw_left = pygame.image.load(bullet_img_left).convert_alpha()
    raw_right = pygame.image.load(bullet_img_right).convert_alpha()

    default_size = (15, 5)

    BULLET_SPRITES["left"] = pygame.transform.smoothscale(raw_left, default_size)
    BULLET_SPRITES["right"] = pygame.transform.smoothscale(raw_right, default_size)


class Bullet(pygame.sprite.Sprite):

    def __init__(self, damage, speed, position, facing_right):

        super().__init__()
        
        self.facing_right = facing_right

        self.image = BULLET_SPRITES["right"]
        self.rect = self.image.get_rect(center = position)

        self.damage = self.__validate_damage(damage)

        self.speed = self.__validate_speed(speed)


    def update(self):

        if self.facing_right:
            self.rect.right += self.speed
        else: self.rect.left -= self.speed

        if self.rect.right < 0 or self.rect.left > default_width:
            self.kill()

    def __validate_damage(self, damage):

        if damage < 0: return default_damage
        return damage

    def __validate_speed(self, speed):

        if speed < 0: return default_bullet_speed
        return speed

