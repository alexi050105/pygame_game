# Plik: GameplayState.py
from Parameters.Imports import *
from States.GameState import GameState
from Entities.Enemy.Enemy import Enemy
from States.MenuState import MenuState
from Entities.Enemy.ArmoredEnemy import ArmoredEnemy
from Entities.Enemy.FastEnemy import FastEnemy
from Entities.HealthPack import HealthPack

if TYPE_CHECKING:
    from Game.Game import Game


class GamePlayState(GameState):
    def __init__(self, manager: "Game") -> None:
        # Inicjalizacja klasy bazowej GameState
        super().__init__(manager)

        # Referencje do ekranu i grup sprite'ow z obiektu Game
        self.screen: pygame.Surface = self.manager.screen
        self.player_group: pygame.sprite.GroupSingle = self.manager.player_group
        self.bullets_group: pygame.sprite.Group = self.manager.bullets_group
        self.enemies_group: pygame.sprite.Group = self.manager.enemies_group
        self.enemies_max_count: int = self.manager.enemies_max_count

        # Referencja do grupy apteczek
        self.healthpacks_group: pygame.sprite.Group = self.manager.healthpacks_group

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            # Wcisniecie ESC powoduje powrot do menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.change_state(MenuState(self.manager))

    def update(self) -> None:
        # Aktualizacja gracza - ruch i strzelanie
        self.player_group.update()

        # Spawning przeciwnikow i apteczek
        self.__spawn_enemies()
        self.__spawn_healthpacks()

        # Ruch przeciwnikow z uwzglednieniem kolizji miedzy nimi
        self.move_and_check_enemy_collisions()

        # Aktualizacja wszystkich grup sprite'ow
        self.healthpacks_group.update()
        self.enemies_group.update()
        self.bullets_group.update()

        # Sprawdzanie kolizji miedzy obiektami
        self.__player_healthpack_collide()
        self.__enemy_bullet_collide()
        self.__enemy_player_collide()

    def move_and_check_enemy_collisions(self) -> None:
        enemies = list(self.enemies_group)

        # Najpierw wszyscy przeciwnicy wykonuja ruch
        for enemy in enemies:
            enemy.move_x()
            enemy.move_y()

        # Kilka iteracji separacji zeby przeciwnicy sie nie nakladali
        for _ in range(default_separation_iterations):
            for i, enemy in enumerate(enemies):
                for j, other in enumerate(enemies):
                    # Pomijamy pary juz sprawdzone i ten sam obiekt
                    if i >= j:
                        continue
                    if not enemy.rect.colliderect(other.rect):
                        continue

                    # Obliczenie wektora miedzy srodkami przeciwnikow
                    dx = enemy.rect.centerx - other.rect.centerx
                    dy = enemy.rect.centery - other.rect.centery

                    # Jesli przeciwnicy sa dokladnie na sobie - losowy kierunek odpychania
                    if dx == 0 and dy == 0:
                        dx = random.choice([-1, 1])
                        dy = random.choice([-1, 1])

                    # Normalizacja wektora odpychania
                    length = (dx ** 2 + dy ** 2) ** 0.5

                    # Obliczenie glebokosci nakladania sie prostokatow
                    overlap_x = (enemy.rect.width // 2 + other.rect.width // 2) - abs(dx)
                    overlap_y = (enemy.rect.height // 2 + other.rect.height // 2) - abs(dy)
                    push = max(overlap_x, overlap_y, 1)

                    nx = dx / length
                    ny = dy / length

                    # Przesun oboje w przeciwnych kierunkach o polowe nakladki
                    enemy.rect.centerx += int(nx * push / default_separation_divisor)
                    enemy.rect.centery += int(ny * push / default_separation_divisor)
                    other.rect.centerx -= int(nx * push / default_separation_divisor)
                    other.rect.centery -= int(ny * push / default_separation_divisor)

                    # Synchronizacja recta dekoratorow z opakowanym przeciwnikiem
                    if hasattr(enemy, '_wrapped'):
                        enemy._wrapped.rect = enemy.rect
                    if hasattr(other, '_wrapped'):
                        other._wrapped.rect = other.rect

    def __enemy_bullet_collide(self) -> None:
        from States.WaveTransitionState import WaveTransitionState
        import Parameters.Imports as assets

        # Sprawdzanie kolizji pociskow z przeciwnikami - pocisk znika, przeciwnik nie
        hits = pygame.sprite.groupcollide(
            self.bullets_group, self.enemies_group, True, False
        )
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                if isinstance(enemy, ArmoredEnemy):
                    # Opancerzony przeciwnik wymaga kilku trafien
                    if enemy.take_hit():
                        enemy.kill()
                        assets.SOUNDS["explosion"].play()
                        self.manager.kills_in_wave += 1
                    else:
                        # Trafiony ale jeszcze zyje
                        assets.SOUNDS["hit"].play()
                else:
                    # Zwykly przeciwnik ginie od jednego trafienia
                    enemy.kill()
                    assets.SOUNDS["explosion"].play()
                    self.manager.kills_in_wave += 1

        # Sprawdzenie czy osiagnieto wymagana liczbe zabitych do przejscia fali
        if self.manager.kills_in_wave >= self.manager.enemies_to_kill:
            self.manager.kills_in_wave = 0
            self.manager.current_wave += 1
            self.manager.enemies_to_kill = default_starting_enemies_to_kill + self.manager.current_wave * default_wave_kills_increment
            self.manager.enemies_max_count = default_starting_enemies_max_count + self.manager.current_wave
            self.manager.change_state(
                WaveTransitionState(self.manager, self.manager.current_wave)
            )

    def __spawn_enemies(self) -> None:
        # Spawning tylko gdy liczba przeciwnikow jest ponizej maksimum
        if len(self.enemies_group) < self.enemies_max_count:
            pos = self.__choose_enemy_pos()
            if not self.player_group.sprite:
                return

            wave = self.manager.current_wave

            # Tworzenie bazowego przeciwnika z HP i predkoscia zalezna od fali
            base = Enemy(
                "Enemy", default_HP + wave * 20,
                pos, default_damage,
                default_enemy_speed,
                self.player_group.sprite
            )

            # Losowe przypisanie dekoratorow w zaleznosci od numeru fali
            enemy = base
            if wave >= default_armored_enemy_min_wave and random.random() < default_armored_enemy_chance:
                enemy = ArmoredEnemy(enemy)
            if wave >= default_fast_enemy_min_wave and random.random() < default_fast_enemy_chance:
                enemy = FastEnemy(enemy)

            self.enemies_group.add(enemy)

    def __enemy_player_collide(self) -> None:
        from States.GameOverState import GameOverState
        import Parameters.Imports as assets

        player = self.player_group.sprite
        if not player:
            return

        # Przeciwnik znika po dotknięciu gracza i zadaje mu obrazenia
        hit_enemies = pygame.sprite.spritecollide(player, self.enemies_group, True)
        for enemy in hit_enemies:
            player.HP -= enemy.damage
            assets.SOUNDS["player_hurt"].play()

            # Jesli HP gracza spadlo do zera lub ponizej - game over
            if player.HP <= 0:
                self.manager.change_state(GameOverState(self.manager))
                return

    def __choose_enemy_pos(self) -> Tuple[int, int]:
        # Losowanie czy przeciwnik pojawi sie po lewej/prawej czy gorze/dole mapy
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

    def __spawn_healthpacks(self) -> None:
        # Zwiekszanie timera co klatke
        self.manager.healthpacks_timer += 1

        # Spawning apteczki gdy timer osiagnie wartosc interwalu
        if self.manager.healthpacks_timer >= self.manager.healthpacks_interval:
            self.manager.healthpacks_timer = 0
            pos = (
                random.randint(50, default_width - 50),
                random.randint(50, default_height - 50)
            )
            self.healthpacks_group.add(HealthPack(pos, default_healthpack_heal))

    def __player_healthpack_collide(self) -> None:
        import Parameters.Imports as assets

        player = self.player_group.sprite
        if not player:
            return

        # Zebranie apteczki przez gracza - przywrocenie HP z limitem do maksimum
        collected = pygame.sprite.spritecollide(player, self.healthpacks_group, True)
        for pack in collected:
            player.HP = min(default_HP, player.HP + pack.heal_amount)
            assets.SOUNDS["healthpack"].play()

    def draw(self) -> None:
        # Rysowanie tla mapy
        self.screen.blit(BACKGROUND, (0, 0))

        # Rysowanie apteczek pod pozostalymi sprite'ami
        self.healthpacks_group.draw(self.screen)

        # Rysowanie gracza, pociskow i przeciwnikow
        self.player_group.draw(self.screen)
        self.bullets_group.draw(self.screen)
        self.enemies_group.draw(self.screen)

        # Rysowanie interfejsu gracza na wierzchu
        self.__draw_hud()

    def __draw_hud(self) -> None:
        player = self.player_group.sprite
        if not player:
            return

        # Rysowanie polprzezroczystego tla pod elementami HUD
        hud_rect = pygame.Rect(5, 5, 220, 80)
        hud_surface = pygame.Surface((hud_rect.width, hud_rect.height), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, default_hud_background_alpha))
        self.screen.blit(hud_surface, (hud_rect.x, hud_rect.y))
        pygame.draw.rect(self.screen, "White", hud_rect, 2)

        # Rysowanie paska HP - czerwone tlo, zielone wypelnienie proporcjonalne do HP
        bar_x, bar_y, bar_w, bar_h = default_hud_bar_x, default_hud_bar_y, default_hud_bar_width, default_hud_bar_height
        ratio = max(0, player.HP / default_HP)
        pygame.draw.rect(self.screen, "DarkRed", (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, "Green", (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(self.screen, "White", (bar_x, bar_y, bar_w, bar_h), 2)

        # Wyswietlanie wartosci HP gracza pod paskiem
        font = pygame.font.Font(default_font, default_font_size_hud)
        hp_surf = font.render(f"HP: {max(0, player.HP)}", False, "White")
        self.screen.blit(hp_surf, (bar_x, bar_y + 22))

        # Wyswietlanie numeru fali i postępu zabic nad paskiem HP
        wave_surf = font.render(
            f"Wave: {self.manager.current_wave} "
            f"({self.manager.kills_in_wave}/{self.manager.enemies_to_kill})",
            False, "White"
        )
        self.screen.blit(wave_surf, (default_hud_bar_x, default_hud_bar_y - 22))