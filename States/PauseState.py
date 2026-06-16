import pygame
from Parameters.DefaultParameters import *
from States.GameState import GameState
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from Game.Game import Game


class PauseState(GameState):
    def __init__(self, manager: "Game") -> None:
        super().__init__(manager)
        self.previous_state = manager.state

        pygame.mixer.music.pause()

        import Parameters.Imports as assets
        FONT = pygame.font.Font(assets.resource_path(default_font), default_font_size)
        FONT_SMALL = pygame.font.Font(assets.resource_path(default_font), default_font_size_small)

        self.title_surf = FONT.render("PAUZA", False, "White")
        self.title_rect = self.title_surf.get_rect(center=(default_width / 2, default_height / 2 - 80))


        self.hint_resume_surf = FONT_SMALL.render("ESC = RETURN TO GAME", False, "Gray")
        self.hint_resume_rect = self.hint_resume_surf.get_rect(center=(default_width / 2, default_height / 2))

        self.hint_settings_surf = FONT_SMALL.render("TAB = SOUND SETTINGS", False, "Gray")
        self.hint_settings_rect = self.hint_settings_surf.get_rect(center=(default_width / 2, default_height / 2 + 40))

        self.hint_menu_surf = FONT_SMALL.render("M = MAIN MENU", False, "Gray")
        self.hint_menu_rect = self.hint_menu_surf.get_rect(center=(default_width / 2, default_height / 2 + 80))

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        from States.MenuState import MenuState
        from States.SettingsState import SettingsState

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.unpause()  # <- wznowienie muzyki
                    self.manager.change_state(self.previous_state)
                elif event.key == pygame.K_m:
                    pygame.mixer.music.unpause()  # <- wznowienie przed resetem (zeby nie zostala zapauzowana)
                    self.__reset_and_go_to_menu()
                elif event.key == pygame.K_TAB:
                    self.manager.change_state(SettingsState(self.manager))

    def __reset_and_go_to_menu(self) -> None:
        from States.MenuState import MenuState

        # Reset stanu fal i przeciwnikow
        self.manager.current_wave = default_starting_wave
        self.manager.kills_in_wave = default_starting_kills
        self.manager.enemies_to_kill = default_starting_enemies_to_kill
        self.manager.enemies_max_count = default_starting_enemies_max_count
        self.manager.enemies_group.empty()
        self.manager.bullets_group.empty()
        self.manager.healthpacks_group.empty()
        self.manager.healthpacks_timer = 0

        # Reset gracza
        player = self.manager.player_group.sprite
        if player:
            player.HP = player.max_HP  # <- zamiast default_HP
            player.rect.center = default_starting_position

        self.manager.change_state(MenuState(self.manager))

    def update(self) -> None:
        # Gra jest zamrozona - nic sie nie aktualizuje
        pass

    def draw(self) -> None:
        self.previous_state.draw()

        overlay = pygame.Surface((default_width, default_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.manager.screen.blit(overlay, (0, 0))

        self.manager.screen.blit(self.title_surf, self.title_rect)
        self.manager.screen.blit(self.hint_resume_surf, self.hint_resume_rect)
        self.manager.screen.blit(self.hint_settings_surf, self.hint_settings_rect)
        self.manager.screen.blit(self.hint_menu_surf, self.hint_menu_rect)