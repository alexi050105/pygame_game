from Parameters.Imports import *
from States.GameState import GameState


class GameOverState(GameState):

    def __init__(self, manager: "Game") -> None:

        super().__init__(manager)

        import Parameters.Imports as assets
        assets.SOUNDS["game_over"].play()
        pygame.mixer.music.stop()

        FONT = pygame.font.Font(default_font, default_font_size)

        FONT_SMALL = pygame.font.Font(default_font, 28)

        self.title_surf = FONT.render("GAME OVER", False, "Red")
        self.title_rect = self.title_surf.get_rect(
            center = (default_width / 2, default_height / 2)
        )

        wave = self.manager.current_wave
        self.into_surf = FONT_SMALL.render(f"You've reached wave:  {self.manager.current_wave}", False, "White")
        self.into_rect = self.into_surf.get_rect(
            center = (default_width / 2, default_height / 2 + 30)
        )

        self.hint_surf = FONT_SMALL.render("PRESS ESC TO TRY AGAIN", False, "Gray")
        self.hint_rect = self.hint_surf.get_rect(
            center = (default_width / 2, default_height / 2 + 80)
        )

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        from States.MenuState import MenuState

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                self.manager.current_wave = default_starting_wave
                self.manager.kills_in_wave = default_starting_kills
                self.manager.enemies_to_kill = default_starting_enemies_to_kill
                self.manager.enemies_max_count = default_starting_enemies_max_count
                self.manager.enemies_group.empty()
                self.manager.bullets_group.empty()
                self.manager.healthpacks_group.empty()
                self.manager.healthpacks_timer = 0

                pygame.mixer.music.load("sounds/happy_adventure.mp3")
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)

                player = self.manager.player_group.sprite

                if player:
                    player.HP = default_HP
                    player.rect.center = default_starting_position
                self.manager.change_state(MenuState(self.manager))

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.manager.screen.fill("Black")
        self.manager.screen.blit(self.title_surf, self.title_rect)
        self.manager.screen.blit(self.into_surf, self.into_rect)
        self.manager.screen.blit(self.hint_surf, self.hint_rect)

