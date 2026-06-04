import random

import pygame

from DefaultParameters import *

from Enemy import *

from abc import ABC, abstractmethod

from random import randrange
class GameState(ABC):
    def __init__(self, manager):
        self.manager = manager

    @abstractmethod
    def handle_event(self, events):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class GameplayState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.screen = self.manager.screen
        self.player_group = self.manager.player_group
        self.bullets_group = self.manager.bullets_group
        self.enemies_group = self.manager.enemies_group
        self.enemies_max_count = self.manager.enemies_max_count

    def handle_event(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state(MenuState(self.manager))

    def update(self) -> None:
        self.player_group.update()
        self.__spawn_enemies()


        self.move_and_check_enemy_collisions()


        self.bullets_group.update()
        self.__enemy_bullet_collide()


    def move_and_check_enemy_collisions(self) -> None:
        for enemy in self.enemies_group:

            enemy.move_x()

            collided = pygame.sprite.spritecollide(enemy, self.enemies_group, False)
            for other in collided:
                if enemy is not other:

                    if enemy.rect.centerx < enemy.player.rect.centerx:
                        enemy.rect.centerx -= enemy.speed
                    else:
                        enemy.rect.centerx += enemy.speed
                    break

            enemy.move_y()

            collided = pygame.sprite.spritecollide(enemy, self.enemies_group, False)
            for other in collided:
                if enemy is not other:

                    if enemy.rect.centery < enemy.player.rect.centery:
                        enemy.rect.centery -= enemy.speed
                    else:
                        enemy.rect.centery += enemy.speed
                    break



    def __enemy_bullet_collide(self):
        pygame.sprite.groupcollide(self.bullets_group,
                                   self.enemies_group,
                                   True, True)

    def __spawn_enemies(self):
        if len(self.enemies_group) < self.enemies_max_count:
            pos = self.__choose_enemy_pos()

            self.enemies_group.add(
                Enemy("Enemy",
                      default_HP,
                      pos,
                      default_damage,
                      default_enemy_speed,
                      self.player_group.sprite
                      )
            )

    def __choose_enemy_pos(self):

        if random.choice([True, False]):

            range_width = [
                (-default_out_of_bounds, 0),
                (default_width, default_width + default_out_of_bounds)
            ]
            chosen_range_x = random.choice(range_width)
            position_x = random.randint(chosen_range_x[0], chosen_range_x[1])


            position_y = random.randint(0, default_height)
        else:

            range_height = [
                (-default_out_of_bounds, 0),
                (default_height, default_height + default_out_of_bounds)
            ]
            chosen_range_y = random.choice(range_height)
            position_y = random.randint(chosen_range_y[0], chosen_range_y[1])


            position_x = random.randint(0, default_width)

        return (position_x, position_y)

    def draw(self):
        self.screen.fill("Blue")
        self.player_group.draw(self.screen)
        self.bullets_group.draw(self.screen)
        self.enemies_group.draw(self.screen)

class MenuState(GameState):
    def __init__(self, manager):
        super().__init__(manager)

        MENU_FONT = pygame.font.Font(default_font)

        self.text_surf = MENU_FONT.render("PRESS ESC TO PLAY", False, "White")
        self.text_rect = self.text_surf.get_rect(center = (default_width/2, default_height/2))

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state(GameplayState(self.manager))

    def update(self):
        pass

    def draw(self):
        self.manager.screen.fill("Green")
        self.manager.screen.blit(self.text_surf, self.text_rect)