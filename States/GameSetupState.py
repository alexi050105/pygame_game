from Parameters.Imports import *
from States.GameState import GameState

if TYPE_CHECKING:
    from Game.Game import Game


class GameSetupState(GameState):
    def __init__(self, manager: "Game") -> None:
        super().__init__(manager)

        import Parameters.Imports as assets
        FONT = pygame.font.Font(assets.resource_path(default_font), default_font_size_small)
        self.title_surf = FONT.render("GAMEPLAY SETTINGS", False, "White")
        self.title_rect = self.title_surf.get_rect(center=(default_width / 2, 100))

        self.hint_surf = FONT.render("ENTER = START   ESC = MENU", False, "Gray")
        self.hint_rect = self.hint_surf.get_rect(center=(default_width / 2, default_height - 60))

        self.difficulty_options = ["EASY", "NORMAL", "HARD"]

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        from States.GamePlayState import GamePlayState
        from States.MenuState import MenuState

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state(MenuState(self.manager))

                elif event.key == pygame.K_RETURN:
                    self.__apply_setup_and_start()
                    self.manager.change_state(GamePlayState(self.manager))

                # Trudnosc - lewo/prawo
                elif event.key == pygame.K_LEFT:
                    self.manager.difficulty_index = max(0, self.manager.difficulty_index - 1)
                elif event.key == pygame.K_RIGHT:
                    self.manager.difficulty_index = min(2, self.manager.difficulty_index + 1)

                # Startowe HP - W/S
                elif event.key == pygame.K_w:
                    self.manager.setup_player_hp = min(max_player_hp, self.manager.setup_player_hp + hp_step)
                elif event.key == pygame.K_s:
                    self.manager.setup_player_hp = max(min_player_hp, self.manager.setup_player_hp - hp_step)

                # Startowa liczba przeciwnikow - A/D
                elif event.key == pygame.K_a:
                    self.manager.setup_enemies_count = max(min_starting_enemies, self.manager.setup_enemies_count - enemies_step)
                elif event.key == pygame.K_d:
                    self.manager.setup_enemies_count = min(max_starting_enemies, self.manager.setup_enemies_count + enemies_step)

    def __apply_setup_and_start(self) -> None:
        enemies_mult = [difficulty_easy_enemies_multiplier, difficulty_normal_enemies_multiplier,
                        difficulty_hard_enemies_multiplier]
        healthpack_mult = [difficulty_easy_healthpack_multiplier, difficulty_normal_healthpack_multiplier,
                           difficulty_hard_healthpack_multiplier]
        decorator_mult = [difficulty_easy_decorator_multiplier, difficulty_normal_decorator_multiplier,
                          difficulty_hard_decorator_multiplier]

        idx = self.manager.difficulty_index
        self.manager.enemies_count_multiplier = enemies_mult[idx]
        self.manager.healthpack_interval_multiplier = healthpack_mult[idx]
        self.manager.decorator_chance_multiplier = decorator_mult[idx]

        player = self.manager.player_group.sprite
        if player:
            player.HP = self.manager.setup_player_hp
            player.max_HP = self.manager.setup_player_hp

        self.manager.enemies_max_count = self.manager.setup_enemies_count

        # enemies_to_kill jest teraz zalezne od liczby przeciwnikow na starcie
        self.manager.enemies_to_kill = self.manager.setup_enemies_count * default_kills_per_enemy_slot

        self.manager.current_wave = default_starting_wave
        self.manager.kills_in_wave = default_starting_kills

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.manager.screen.fill("Black")
        self.manager.screen.blit(self.title_surf, self.title_rect)

        import Parameters.Imports as assets
        font = pygame.font.Font(assets.resource_path(default_font), default_font_size_hud)

        diff_text = self.difficulty_options[self.manager.difficulty_index]
        diff_surf = font.render(f"DIFFICULTY: {diff_text}  (arrowkeys left/right)", False, "White")
        diff_rect = diff_surf.get_rect(center=(default_width / 2, 250))
        self.manager.screen.blit(diff_surf, diff_rect)

        hp_surf = font.render(f"STARTING HP: {self.manager.setup_player_hp}  (W/S)", False, "White")
        hp_rect = hp_surf.get_rect(center=(default_width / 2, 320))
        self.manager.screen.blit(hp_surf, hp_rect)

        enemies_surf = font.render(f"STARTING ENEMIES COUNT: {self.manager.setup_enemies_count}  (A/D)", False, "White")
        enemies_rect = enemies_surf.get_rect(center=(default_width / 2, 390))
        self.manager.screen.blit(enemies_surf, enemies_rect)

        self.manager.screen.blit(self.hint_surf, self.hint_rect)