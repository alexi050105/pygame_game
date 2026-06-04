import pygame

from abc import ABC, abstractmethod

from DefaultParameters import *
class Person(pygame.sprite.Sprite, ABC):

    def __init__(self, name, HP, starting_position, damage, speed):
        super().__init__()

        self.name = name
        self.HP = self.__validate_HP(HP)
        self.starting_position = self.__validate_starting_position(starting_position)
        self.damage = self.__validate_damage(damage)
        self.speed = self.__validate_speed(speed)

        self.facing_right = None

        self.image = None
        self.rect = None

    def update(self):
        self.update()

    def update(self):
        keys = pygame.key.get_pressed()

        # ruszanie sie po osi y
        if keys[pygame.K_w]:
            self.__move_up()
        elif keys[pygame.K_s]:
            self.__move_down()

        # ruszanie sie po osi x
        if keys[pygame.K_a]:
            self.__move_left()
        elif keys[pygame.K_d]:
            self.__move_right()

    def __validate_HP(self, HP):
        if HP <= 0: return default_HP
        return HP

    def __validate_speed(self, speed):
        if speed < 0: return default_player_speed
        return speed

    def __validate_damage(self, damage):
        if damage < 0: return default_damage
        return damage

    def __validate_starting_position(self, starting_position):
        if (starting_position[0] < -default_out_of_bounds
            or
            starting_position[0] > default_width + default_out_of_bounds):
            start_x = default_width / 2
        else: start_x = starting_position[0]

        if (starting_position[1] < - default_out_of_bounds
            or
            starting_position[1] > default_height + default_out_of_bounds):
            start_y = default_height / 2
        else: start_y = starting_position[1]

        return (start_x, start_y)


    def __move_up(self):
        self.rect.top -= self.speed
        if self.rect.top < -default_out_of_bounds:
            self.rect.top = -default_out_of_bounds

    def __move_down(self):
        self.rect.bottom += self.speed
        if self.rect.bottom > (default_height + default_out_of_bounds):
            self.rect.bottom = default_height + default_out_of_bounds

    def __move_left(self):
        self.rect.left -= self.speed
        self.facing_right = False
        if self.rect.left < -default_out_of_bounds:
            self.rect.left = -default_out_of_bounds

    def __move_right(self):
        self.rect.right += self.speed
        self.facing_right = True
        if self.rect.right > (default_height + default_out_of_bounds):
            self.rect.right = default_height + default_out_of_bounds