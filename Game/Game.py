# Plik: Game.py
from Parameters.Imports import *
from Entities.Player import Player
from States.MenuState import MenuState
from States.GameState import GameState


class Game:
    def __init__(self) -> None:
        # Inicjalizacja pygame i modulu wyswietlania
        pygame.init()
        pygame.display.init()

        pygame.display.set_caption('Beware of the WOLVES')

        # Ustawienie rozdzielczosci okna gry na podstawie parametrow domyslnych
        self.resolution: Tuple[int, int] = (default_width, default_height)
        self.screen: pygame.Surface = pygame.display.set_mode(self.resolution)

        # Ladowanie wszystkich grafik i dzwiekow przed uruchomieniem gry
        load_all_game_images()
        load_all_game_sounds()

        # Zaladowanie i odtworzenie muzyki w tle w petli (-1 oznacza nieskonczone zapetlenie)
        pygame.mixer.music.load("sounds/happy_adventure.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        # Grupy sprite'ow do zarzadzania pociskami i przeciwnikami
        self.bullets_group: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies_group: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies_max_count: int = 10

        # Tworzenie gracza i dodanie go do grupy pojedynczego sprite'a
        self.player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.player_group.add(
            Player("Player", default_HP, default_starting_position,
                   default_player_damage, default_player_speed, self.bullets_group)
        )

        # Grupa apteczek oraz timer kontrolujacy czestotliwosc ich pojawiania sie
        self.healthpacks_group: pygame.sprite.Group = pygame.sprite.Group()
        self.healthpacks_timer: int = 0
        self.healthpacks_interval: int = default_fps * 5

        # Zmienne do sledzenia postepu fal - numer fali, liczba zabic i limity
        self.current_wave: int = 1
        self.kills_in_wave: int = 0
        self.enemies_to_kill: int = 5
        self.enemies_max_count: int = 3

        # Zegar do kontrolowania liczby klatek na sekunde
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Ustawienie poczatkowego stanu gry na menu glowne (wzorzec Stan)
        self.state: GameState = MenuState(self)
        self.running: bool = True

    def run(self) -> None:
        # Glowna petla gry - dziala dopoki self.running jest True
        while self.running:
            # Pobieranie wszystkich zdarzen pygame (klawiatura, mysz, zamkniecie okna)
            events = pygame.event.get()
            for event in events:
                # Obsluga zamkniecia okna przez uzytkownika
                if event.type == pygame.QUIT:
                    self.running = False

            # Delegowanie obslugi zdarzen, aktualizacji i rysowania do aktualnego stanu
            self.state.handle_event(events)
            self.state.update()
            self.state.draw()

            # Odswiezenie ekranu i ograniczenie FPS do wartosci domyslnej
            pygame.display.update()
            self.clock.tick(default_fps)

        # Zatrzymanie pygame i wyjscie z programu po zakonczeniu petli
        pygame.quit()
        quit()

    def change_state(self, state: GameState) -> None:
        # Zmiana aktualnego stanu gry - realizacja wzorca Stan
        self.state = state