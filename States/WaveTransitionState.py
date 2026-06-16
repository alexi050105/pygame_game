from Parameters.Imports import *
from States.GameState import GameState


# Klasa obslugujaca stan przejscia miedzy falami (np. wyswietlanie napisu "Wave X!")
class WaveTransitionState(GameState):

    def __init__(self, manager: "Game", wave_number: int) -> None:
        # Inicjalizacja klasy bazowej GameState
        super().__init__(manager)

        # Lokalny import zasobow w celu odtworzenia dzwieku nowej fali
        import Parameters.Imports as assets
        assets.SOUNDS["wave"].play()

        # Ustawienie timera trwania ekranu przejscia (2 sekundy, zalezne od FPS)
        self.timer: int = default_fps * 2

        # Inicjalizacja czcionki oraz wyrenderowanie tekstu z numerem fali
        FONT = pygame.font.Font(assets.resource_path(default_font), default_font_size)
        self.text_surf = FONT.render(f"Wave {wave_number}!", False, "White")

        # Wycentrowanie tekstu na srodku ekranu gry
        self.text_rect = self.text_surf.get_rect(
            center=(default_width / 2, default_height / 2)
        )

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        # Brak obslugi zdarzen wejsciowych (np. klikniec) podczas tego stanu
        pass

    def update(self) -> None:
        from States.GamePlayState import GamePlayState

        # Odliczanie czasu trwania stanu przejscia
        self.timer -= 1

        # Kiedy timer dojdzie do zera, nastepuje reset i przejscie do nowej fali
        if self.timer <= 0:

            # Czyszczenie grup przeciwnikow oraz pociskow przed nowa fala
            self.manager.enemies_group.empty()
            self.manager.bullets_group.empty()

            # Resetowanie pozycji gracza na srodek ekranu, jesli gracz istnieje
            player = self.manager.player_group.sprite
            if player:
                player.rect.center = (default_width / 2, default_height / 2)

            # Zmiana stanu gry z powrotem na glowna rozgrywke (GamePlayState)
            self.manager.change_state(GamePlayState(self.manager))

    def draw(self) -> None:
        # Czyszczenie ekranu kolorem czarnym
        self.manager.screen.fill("Black")
        # Rysowanie wyrenderowanego tekstu z numerem fali na ekranie
        self.manager.screen.blit(self.text_surf, self.text_rect)