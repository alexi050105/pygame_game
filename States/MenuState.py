import pygame
# 1. ZAMIENIAMY "import *" NA IMPORT CALEGO MODULU
import Parameters.Imports as GameImports
from States.GameState import GameState
from typing import TYPE_CHECKING, List

# Zapobieganie cyklicznym importom dzieki TYPE_CHECKING (uzywane tylko przez lintery i IDE)
if TYPE_CHECKING:
    from Game.Game import Game


# Klasa reprezentujaca stan menu glownego gry, dziedziczaca po bazowej klasie GameState
class MenuState(GameState):
    def __init__(self, manager: "Game") -> None:
        # Inicjalizacja klasy bazowej i przypisanie managera stanu gry
        super().__init__(manager)

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        # Import lokalny, aby uniknac bledu cyklicznego importu (Circular Import)
        from States.GamePlayState import GamePlayState

        # Przetwarzanie listy zdarzen
        for event in events:
            # Jesli gracz nacisnie klawisz ESCAPE, nastepuje powrot lub przejscie do rozgrywki
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.change_state(GamePlayState(self.manager))

    def update(self) -> None:
        # Aktualizacja logiki menu
        pass

    def draw(self) -> None:
        # Rysowanie tla menu na ekranie
        self.manager.screen.blit(GameImports.BACKGROUND_MENU, (0, 0))