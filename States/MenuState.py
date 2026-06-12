import pygame
# 1. ZAMIENIAMY "import *" NA IMPORT CAŁEGO MODUŁU
import Parameters.Imports as GameImports
from States.GameState import GameState
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from Game.Game import Game

class MenuState(GameState):
    def __init__(self, manager: "Game") -> None:
        super().__init__(manager)


    def handle_event(self, events: List[pygame.event.Event]) -> None:
        from States.GamePlayState import GamePlayState
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.change_state(GamePlayState(self.manager))

    def update(self) -> None:
        pass

    def draw(self) -> None:
        # 3. KLUCZOWA ZMIANA: Pobieramy aktualną wartość BACKGROUND_MENU z modułu
        self.manager.screen.blit(GameImports.BACKGROUND_MENU, (0, 0))
