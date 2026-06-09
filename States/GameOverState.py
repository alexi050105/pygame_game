from Parameters.Imports import *
from States.GameState import GameState


class GameOverState(GameState):

    def __init__(self, manager: "Game") -> None:

        super().__init__(manager)

        FONT = pygame.font.Font(default_font, default_font_size)

        FONT_SMALL = pygame.font.Font(default_font, 28)

        self.title_surf = FONT.render("GAME OVER", False, "Red")
        self.title_rect = self.title_surf.get_rect(
            center = (default_width / 2, default_height / 2)
        )

        wave = self.manager.current_wave
        self.into_surf = FONT_SMALL.render("You've reached wave: {wave}", False, "White")
        self.into_rect = self.into_surf.get_rect(
            center = (default_width / 2, default_height / 2 + 20)
        )

        self.hint_surf = FONT_SMALL.render("ESC = MENU", False, "Gray")
        self.hint_rect = self.hint_surf.get_rect(
            center = (default_width / 2, default_height / 2 + 70)
        )

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        from States.MenuState import MenuState

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                self.manager.current_wave = 1
                self.manager.kills_in_wave = 0
                self.manager.enemies_to_kill = 5
                self.manager.enemies_max_count = 3
                self.manager.enemies_group.empty()
                self.manager.bullets_group.empty()

                player = self.manager.player_group.sprite

                if player:
                    player.HP = default_HP
                self.manager.change_state(MenuState(self.manager))

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.manager.screen.fill("Black")
        self.manager.screen.blit(self.title_surf, self.title_rect)
        self.manager.screen.blit(self.into_surf, self.into_rect)
        self.manager.screen.blit(self.hint_surf, self.hint_rect)

