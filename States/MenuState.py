import pygame
import Parameters.Imports as GameImports
from Parameters.DefaultParameters import *
from States.GameState import GameState
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from Game.Game import Game


class MenuState(GameState):
    def __init__(self, manager: "Game") -> None:
        super().__init__(manager)

        MENU_FONT = pygame.font.Font(GameImports.resource_path(default_font), default_font_size)
        self.text_surf = MENU_FONT.render("", False, "White")
        self.text_rect = self.text_surf.get_rect(center=(default_width / 2, default_height / 2))

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        from States.GameSetupState import GameSetupState
        from States.SettingsState import SettingsState
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state(GameSetupState(self.manager))
                elif event.key == pygame.K_TAB:
                    self.manager.change_state(SettingsState(self.manager))

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.manager.screen.blit(GameImports.BACKGROUND_MENU, (0, 0))
        self.manager.screen.blit(self.text_surf, self.text_rect)

        font = pygame.font.Font(GameImports.resource_path(default_font), default_font_size_small)
        tab_hint = font.render("TAB = SOUND SETTINGS", False, "White")
        tab_rect = tab_hint.get_rect(center=(default_width / 2, default_height / 2 + 120))
        self.manager.screen.blit(tab_hint, tab_rect)
