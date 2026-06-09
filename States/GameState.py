# Plik: GameState.py
from Parameters.Imports import *

if TYPE_CHECKING:
    from Game.Game import Game

class GameState(ABC):
    def __init__(self, manager: "Game") -> None:
        self.manager: "Game" = manager

    @abstractmethod
    def handle_event(self, events: List[pygame.event.Event]) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass