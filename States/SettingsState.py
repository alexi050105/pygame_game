from Parameters.Imports import *
from States.GameState import GameState

if TYPE_CHECKING:
    from Game.Game import Game


class SettingsState(GameState):
    def __init__(self, manager: "Game") -> None:
        super().__init__(manager)
        self.previous_state = manager.state

        import Parameters.Imports as assets
        FONT = pygame.font.Font(assets.resource_path(default_font), default_font_size_small)
        self.title_surf = FONT.render("SOUND SETTINGS", False, "White")
        self.title_rect = self.title_surf.get_rect(center=(default_width / 2, 150))

        self.hint_surf = FONT.render("ESC = return", False, "Gray")
        self.hint_rect = self.hint_surf.get_rect(center=(default_width / 2, default_height - 80))

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        import Parameters.Imports as assets
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state(self.previous_state)
                # Glosnosc muzyki
                elif event.key == pygame.K_UP:
                    self.manager.music_volume = min(1.0, self.manager.music_volume + default_volume_step)
                    pygame.mixer.music.set_volume(self.manager.music_volume)
                elif event.key == pygame.K_DOWN:
                    self.manager.music_volume = max(0.0, self.manager.music_volume - default_volume_step)
                    pygame.mixer.music.set_volume(self.manager.music_volume)
                # Glosnosc efektow
                elif event.key == pygame.K_RIGHT:
                    self.manager.sfx_volume = min(1.0, self.manager.sfx_volume + default_volume_step)
                    self.__apply_sfx_volume()
                elif event.key == pygame.K_LEFT:
                    self.manager.sfx_volume = max(0.0, self.manager.sfx_volume - default_volume_step)
                    self.__apply_sfx_volume()

    def __apply_sfx_volume(self) -> None:
        import Parameters.Imports as assets
        for sound in assets.SOUNDS.values():
            sound.set_volume(self.manager.sfx_volume)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.manager.screen.fill("Black")
        self.manager.screen.blit(self.title_surf, self.title_rect)

        import Parameters.Imports as assets
        font = pygame.font.Font(assets.resource_path(default_font), default_font_size_hud)

        music_surf = font.render(
            f"MUSIC: {int(self.manager.music_volume * 100)}%  (W/S arrowkeys up/down)",
            False, "White"
        )
        music_rect = music_surf.get_rect(center=(default_width / 2, 300))
        self.manager.screen.blit(music_surf, music_rect)

        sfx_surf = font.render(
            f"EFFECTS: {int(self.manager.sfx_volume * 100)}%  (arrowkeys left/right)",
            False, "White"
        )
        sfx_rect = sfx_surf.get_rect(center=(default_width / 2, 360))
        self.manager.screen.blit(sfx_surf, sfx_rect)

        self.manager.screen.blit(self.hint_surf, self.hint_rect)