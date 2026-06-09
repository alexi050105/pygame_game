# Plik: GameplayState.py
import pygame
from Parameters.Imports import *
from States.GameState import GameState
from Entities.Enemy import Enemy
from States.MenuState import MenuState

from Entities.ArmoredEnemy import ArmoredEnemy
from Entities.FastEnemy import FastEnemy

if TYPE_CHECKING:
    from Game.Game import Game

class GameplayState(GameState):
    def __init__(self, manager: "Game") -> None:

        super().__init__(manager)

        self.screen: pygame.Surface = self.manager.screen
        self.player_group: pygame.sprite.GroupSingle = self.manager.player_group
        self.bullets_group: pygame.sprite.Group = self.manager.bullets_group
        self.enemies_group: pygame.sprite.Group = self.manager.enemies_group
        self.enemies_max_count: int = self.manager.enemies_max_count

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.change_state(MenuState(self.manager))

    def update(self) -> None:
        self.player_group.update()
        self.__spawn_enemies()
        self.move_and_check_enemy_collisions()
        self.enemies_group.update()
        self.bullets_group.update()
        self.__enemy_bullet_collide()
        self.__enemy_player_collide()

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

    def __enemy_bullet_collide(self) -> None:
        from States.WaveTransitionState import WaveTransitionState
        hits = pygame.sprite.groupcollide(
            self.bullets_group, self.enemies_group, True, False  # dokill=False
        )
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                if isinstance(enemy, ArmoredEnemy):
                    if enemy.take_hit():  # True = zgon
                        enemy.kill()
                        self.manager.kills_in_wave += 1
                else:
                    enemy.kill()
                    self.manager.kills_in_wave += 1

        if self.manager.kills_in_wave >= self.manager.enemies_to_kill:
            self.manager.kills_in_wave = 0
            self.manager.current_wave += 1
            self.manager.enemies_to_kill = 5 + self.manager.current_wave * 3
            self.manager.enemies_max_count = 3 + self.manager.current_wave
            self.manager.change_state(
                WaveTransitionState(self.manager, self.manager.current_wave)
            )

    def __spawn_enemies(self) -> None:
        if len(self.enemies_group) < self.enemies_max_count:
            pos = self.__choose_enemy_pos()
            if not self.player_group.sprite:
                return

            wave = self.manager.current_wave
            base = Enemy(
                "Enemy", default_HP + wave * 20,
                pos, default_damage,
                default_enemy_speed,
                self.player_group.sprite
            )

            # Fala 2+ : 30% szans na szybkiego
            # Fala 3+ : 30% szans na opancerzonego
            # Można też stackować oba naraz
            enemy = base
            if wave >= 3 and random.random() < 0.3:
                enemy = ArmoredEnemy(enemy)
            if wave >= 2 and random.random() < 0.3:
                enemy = FastEnemy(enemy)

            self.enemies_group.add(enemy)

    def __enemy_player_collide(self) -> None:
        from States.GameOverState import GameOverState

        player = self.player_group.sprite

        if not player:
            return

        hit_enemies = pygame.sprite.spritecollide(player, self.enemies_group, True)

        for enemy in hit_enemies:
            player.HP -= enemy.damage
            if player.HP <= 0:
                self.manager.change_state(GameOverState(self.manager))
                return

    def __choose_enemy_pos(self) -> Tuple[int, int]:
        if random.choice([True, False]):
            range_width = [(-default_out_of_bounds, 0), (default_width, default_width + default_out_of_bounds)]
            chosen_range_x = random.choice(range_width)
            position_x = random.randint(chosen_range_x[0], chosen_range_x[1])
            position_y = random.randint(0, default_height)
        else:
            range_height = [(-default_out_of_bounds, 0), (default_height, default_height + default_out_of_bounds)]
            chosen_range_y = random.choice(range_height)
            position_y = random.randint(chosen_range_y[0], chosen_range_y[1])
            position_x = random.randint(0, default_width)
        return (position_x, position_y)

    def draw(self) -> None:
        self.screen.fill("Blue")
        self.player_group.draw(self.screen)
        self.bullets_group.draw(self.screen)
        self.enemies_group.draw(self.screen)
        self.__draw_hud()

    def __draw_hud(self) -> None:
        player = self.player_group.sprite
        if not player:
            return

        bar_x, bar_y, bar_w, bar_h = 10, 40, 200, 18
        ratio = max(0, player.HP / default_HP)
        pygame.draw.rect(self.screen, "DarkRed", (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, "Green", (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(self.screen, "White", (bar_x, bar_y, bar_w, bar_h), 2)

        font = pygame.font.Font(default_font, 20)
        hp_surf = font.render(f"HP: {max(0, player.HP)}", False, "White")
        self.screen.blit(hp_surf, (bar_x, bar_y + 22))

        wave_surf = font.render(
            f"Fala: {self.manager.current_wave}  "
            f"Kills: {self.manager.kills_in_wave}/{self.manager.enemies_to_kill}",
            False, "White"
        )
        self.screen.blit(wave_surf, (10, 10))




