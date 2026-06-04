from Player import *

from States.GameState import *

from Bullet import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.init()


        self.resolution = (default_width, default_height)
        self.screen = pygame.display.set_mode(self.resolution)

        load_player_images()
        load_enemy_images()
        load_bullet_images()

        self.bullets_group = pygame.sprite.Group()

        self.enemies_group = pygame.sprite.Group()
        self.enemies_max_count = 10

        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(
            Player("Player", default_HP, default_starting_position,
                   default_player_damage, default_player_speed, self.bullets_group))

        self.score = 0
        self.clock = pygame.time.Clock()
        self.state = MenuState(self)
        self.running = True

    def run(self):
        while self.running:
            # 1. Jedyne pobranie eventów w całej grze!
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # 2. Przekazujemy eventy do stanu
            self.state.handle_event(events)

            # 3. Aktualizujemy logikę stanu
            self.state.update()

            # 4. Rysujemy stan
            self.state.draw()

            # 5. Globalne odświeżenie ekranu i zegar dla każdego stanu!
            pygame.display.update()
            self.clock.tick(default_fps)

        pygame.quit()
        quit()

    def change_state(self, state):
        self.state = state