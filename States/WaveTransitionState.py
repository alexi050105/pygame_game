from Parameters.Imports import *
from States.GameState import GameState

class WaveTransitionState(GameState):

    def __init__(self, manager: "Game", wave_number: int) -> None:

        super().__init__(manager)

        import Parameters.Imports as assets
        assets.SOUNDS["wave"].play()

        self.timer: int = default_fps * 2

        FONT = pygame.font.Font(default_font, default_font_size)
        self.text_surf = FONT.render(f"Wave {wave_number}!", False, "White")
        self.text_rect = self.text_surf.get_rect(
            center = (default_width / 2, default_height / 2)
        )

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        pass

    def update(self) -> None:
        from States.GamePlayState import GamePlayState

        self.timer -= 1

        if self.timer <= 0:

            self.manager.enemies_group.empty()
            self.manager.bullets_group.empty()

            player = self.manager.player_group.sprite
            if player:
                player.rect.center = (default_width / 2, default_height / 2)

            self.manager.change_state(GamePlayState(self.manager))

    def draw(self) -> None:
        self.manager.screen.fill("Black")
        self.manager.screen.blit(self.text_surf, self.text_rect)


