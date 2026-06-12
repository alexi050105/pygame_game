# Plik: GameState.py
from Parameters.Imports import *

if TYPE_CHECKING:
    from Game.Game import Game


class GameState(ABC):
    def __init__(self, manager: "Game") -> None:
        # Referencja do glownego obiektu gry umozliwiajaca dostep do grup sprite'ow i zmiennych
        self.manager: "Game" = manager

    @abstractmethod
    def handle_event(self, events: List[pygame.event.Event]) -> None:
        # Abstrakcyjna metoda obslugi zdarzen - kazdy stan implementuje ja inaczej
        pass

    @abstractmethod
    def update(self) -> None:
        # Abstrakcyjna metoda aktualizacji logiki stanu - wywoływana co klatke
        pass

    @abstractmethod
    def draw(self) -> None:
        # Abstrakcyjna metoda rysowania stanu - wywoływana co klatke po update()
        pass