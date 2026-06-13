import pytest
import pygame
import os


# Fixture uruchamiana automatycznie przed kazdym testem (autouse=True)
@pytest.fixture(autouse=True)
def init_pygame():
    # Ustawienie zmiennych srodowiskowych dla SDL, aby uruchomic Pygame w trybie bezokienkowym (headless)
    # Dzieki temu testy moga dzialac na serwerach CI/CD bez fizycznego ekranu i karty dzwiekowej
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"

    # Inicjalizacja modulow Pygame oraz utworzenie wirtualnego ekranu
    pygame.init()
    pygame.display.set_mode((800, 800))

    # Tworzenie pustych obiektow Surface (atrap/mockow tekstur) na potrzeby testow
    dummy_50 = pygame.Surface((50, 50), pygame.SRCALPHA)
    dummy_bullet = pygame.Surface((15, 5))

    # Importowanie modulu zasobow gry, aby podmienic prawdziwe pliki graficzne na przygotowane atrapy
    from Parameters import Imports

    # Podmienianie tekstur gracza
    Imports.PLAYER_SPRITES["left"] = dummy_50
    Imports.PLAYER_SPRITES["right"] = dummy_50

    # Podmienianie tekstur podstawowego przeciwnika (Base Enemy)
    Imports.BASE_ENEMY_SPRITES["left"] = dummy_50
    Imports.BASE_ENEMY_SPRITES["right"] = dummy_50
    Imports.BASE_ENEMY_SPRITES["up"] = dummy_50
    Imports.BASE_ENEMY_SPRITES["down"] = dummy_50

    # Podmienianie tekstur szybkiego przeciwnika (Fast Enemy)
    Imports.FAST_ENEMY_SPRITES["left"] = dummy_50
    Imports.FAST_ENEMY_SPRITES["right"] = dummy_50
    Imports.FAST_ENEMY_SPRITES["up"] = dummy_50
    Imports.FAST_ENEMY_SPRITES["down"] = dummy_50

    # Podmienianie tekstur opancerzonego przeciwnika (Armored Enemy)
    Imports.ARMORED_ENEMY_SPRITES["left"] = dummy_50
    Imports.ARMORED_ENEMY_SPRITES["right"] = dummy_50
    Imports.ARMORED_ENEMY_SPRITES["up"] = dummy_50
    Imports.ARMORED_ENEMY_SPRITES["down"] = dummy_50

    # Podmienianie tekstur pociskow oraz apteczki
    Imports.BULLET_SPRITES["left"] = dummy_bullet
    Imports.BULLET_SPRITES["right"] = dummy_bullet
    Imports.HEALTHPACK_SPRITE = pygame.Surface((40, 30), pygame.SRCALPHA)

    # Tworzenie atrap dzwiekow w pamieci RAM (pusta tablica bajtow) zamiast ladowania plikow .wav/.mp3
    dummy_sound = pygame.mixer.Sound(buffer=bytes(44))

    # Przypisanie wirtualnego dzwieku do wszystkich efektow dzwiekowych uzywanych w grze
    for key in ["shoot", "explosion", "hit", "wave", "healthpack", "player_hurt", "game_over"]:
        Imports.SOUNDS[key] = dummy_sound

    # W tym miejscu nastepuje wykonanie wlasciwego testu
    yield

    # Sprzatanie po zakonczeniu testu - zamkniecie wszystkich modulow Pygame
    pygame.quit()