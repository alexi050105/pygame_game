# Plik: MenuState.py
from Parameters.Imports import *
from States.GameState import GameState

if TYPE_CHECKING:
    from Game.Game import Game

class MenuState(GameState):
    def __init__(self, manager: "Game") -> None:
        super().__init__(manager)
        MENU_FONT = pygame.font.Font(default_font, default_font_size)
        self.text_surf = MENU_FONT.render("PRESS ESC TO PLAY", False, "White")
        self.text_rect = self.text_surf.get_rect(center=(default_width / 2, default_height / 2))

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        from States.GameplayState import GameplayState  # Import lokalny unikający kolizji
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.manager.change_state(GameplayState(self.manager))

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.manager.screen.fill("Green")
        self.manager.screen.blit(self.text_surf, self.text_rect)