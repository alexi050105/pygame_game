# Plik: Game.py
from Parameters.Imports import *
from Entities.Player import Player
from States.MenuState import MenuState
from States.GameState import GameState


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.init()

        self.resolution: Tuple[int, int] = (default_width, default_height)
        self.screen: pygame.Surface = pygame.display.set_mode(self.resolution)

        # Wywołujemy ładowanie grafik z pliku agregującego
        load_all_game_images()
        load_all_game_sounds()

        pygame.mixer.music.load("sounds/happy_adventure.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)  # -1 = zapętlenie

        self.bullets_group: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies_group: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies_max_count: int = 10

        self.player_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
        self.player_group.add(
            Player("Player", default_HP, default_starting_position,
                   default_player_damage, default_player_speed, self.bullets_group)
        )

        self.healthpacks_group: pygame.sprite.Group = pygame.sprite.Group()
        self.healthpacks_timer: int = 0
        self.healthpacks_interval: int = default_fps * 5

        self.current_wave: int = 1
        self.kills_in_wave: int = 0
        self.enemies_to_kill: int = 5
        self.enemies_max_count: int = 3

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.state: GameState = MenuState(self)
        self.running: bool = True

    def run(self) -> None:
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.handle_event(events)
            self.state.update()
            self.state.draw()

            pygame.display.update()
            self.clock.tick(default_fps)

        pygame.quit()
        quit()

    def change_state(self, state: GameState) -> None:
        self.state = state