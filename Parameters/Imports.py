# Plik: Imports.py
import sys
import os
import random
import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple

# Importujemy wszystkie parametry domyslne
from Parameters.DefaultParameters import *

# Globalne slowniki przechowujace sprite'y postaci i obiektow
PLAYER_SPRITES = {}
BASE_ENEMY_SPRITES = {}
FAST_ENEMY_SPRITES = {}
ARMORED_ENEMY_SPRITES = {}
BULLET_SPRITES = {}

# Globalne zmienne na tla i sprite apteczki - inicjowane w load_all_game_images()
BACKGROUND = None
HEALTHPACK_SPRITE = None
BACKGROUND_MENU = None

# Globalny slownik dzwiekow - inicjowany w load_all_game_sounds()
SOUNDS = {}
MUSIC_PATH = "sounds/happy_adventure.mp3"


def resource_path(relative_path: str) -> str:
    """Zwraca poprawna sciezke do pliku - dziala zarowno w PyCharmie jak i po spakowaniu do exe przez PyInstaller."""
    try:
        # PyInstaller tworzy folder tymczasowy i zapisuje jego sciezke w sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # W trakcie normalnego uruchamiania uzywamy biezacego katalogu
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_all_game_images() -> None:
    global PLAYER_SPRITES, \
        BASE_ENEMY_SPRITES, \
        FAST_ENEMY_SPRITES, \
        ARMORED_ENEMY_SPRITES, \
        BULLET_SPRITES, BACKGROUND, HEALTHPACK_SPRITE, BACKGROUND_MENU

    # Ladowanie tla menu glownego
    raw_menu = pygame.image.load(resource_path("graphics/menu.png")).convert()
    BACKGROUND_MENU = pygame.transform.scale(raw_menu, (default_width, default_height))

    # Rozmiar sprite'ow przeciwnikow
    enemy_size = (64, 41)

    # Ladowanie sprite'a apteczki
    raw_hp = pygame.image.load(resource_path("graphics/burger.png")).convert_alpha()
    HEALTHPACK_SPRITE = pygame.transform.scale(raw_hp, (32, 32))

    # Ladowanie tla mapy gry
    raw_bg = pygame.image.load(resource_path("graphics/map.png")).convert()
    BACKGROUND = pygame.transform.smoothscale(raw_bg, (default_width, default_height))

    # 1. Sprite'y gracza - wersja lewa i prawa
    raw_p_left = pygame.image.load(resource_path("graphics/player_left.png")).convert_alpha()
    raw_p_right = pygame.image.load(resource_path("graphics/player_right.png")).convert_alpha()
    PLAYER_SPRITES["left"] = pygame.transform.scale(raw_p_left, (46, 76))
    PLAYER_SPRITES["right"] = pygame.transform.scale(raw_p_right, (46, 76))

    # 2. Sprite'y podstawowego przeciwnika - wersja lewa i prawa
    raw_b_e_left = pygame.image.load(resource_path("graphics/default_enemy_left.png")).convert_alpha()
    raw_b_e_right = pygame.image.load(resource_path("graphics/default_enemy_right.png")).convert_alpha()
    BASE_ENEMY_SPRITES["left"] = pygame.transform.scale(raw_b_e_left, enemy_size)
    BASE_ENEMY_SPRITES["right"] = pygame.transform.scale(raw_b_e_right, enemy_size)

    # Sprite'y szybkiego przeciwnika - wersja lewa i prawa
    raw_f_e_left = pygame.image.load(resource_path("graphics/fast_enemy_left.png")).convert_alpha()
    raw_f_e_right = pygame.image.load(resource_path("graphics/fast_enemy_right.png")).convert_alpha()
    FAST_ENEMY_SPRITES["left"] = pygame.transform.scale(raw_f_e_left, enemy_size)
    FAST_ENEMY_SPRITES["right"] = pygame.transform.scale(raw_f_e_right, enemy_size)

    # Sprite'y opancerzonego przeciwnika - wersja lewa i prawa
    raw_ar_e_left = pygame.image.load(resource_path("graphics/armored_enemy_left.png")).convert_alpha()
    raw_ar_e_right = pygame.image.load(resource_path("graphics/armored_enemy_right.png")).convert_alpha()
    ARMORED_ENEMY_SPRITES["left"] = pygame.transform.scale(raw_ar_e_left, enemy_size)
    ARMORED_ENEMY_SPRITES["right"] = pygame.transform.scale(raw_ar_e_right, enemy_size)

    # 3. Sprite'y pocisku - wersja lewa i prawa
    raw_b_left = pygame.image.load(resource_path("graphics/bullet_left.png")).convert_alpha()
    raw_b_right = pygame.image.load(resource_path("graphics/bullet_right.png")).convert_alpha()
    BULLET_SPRITES["left"] = pygame.transform.smoothscale(raw_b_left, (15, 5))
    BULLET_SPRITES["right"] = pygame.transform.smoothscale(raw_b_right, (15, 5))


def load_all_game_sounds() -> None:
    global SOUNDS

    # Ladowanie plikow dzwiekowych do slownika
    SOUNDS["shoot"] = pygame.mixer.Sound(resource_path("sounds/click.wav"))
    SOUNDS["explosion"] = pygame.mixer.Sound(resource_path("sounds/explosion.wav"))
    SOUNDS["hit"] = pygame.mixer.Sound(resource_path("sounds/hitHurt.wav"))
    SOUNDS["wave"] = pygame.mixer.Sound(resource_path("sounds/jump.wav"))
    SOUNDS["healthpack"] = pygame.mixer.Sound(resource_path("sounds/powerUp.wav"))
    SOUNDS["player_hurt"] = pygame.mixer.Sound(resource_path("sounds/playerHurt.wav"))
    SOUNDS["game_over"] = pygame.mixer.Sound(resource_path("sounds/gameOver.wav"))

    # Ustawienie glosnosci dla kazdego dzwieku na podstawie parametrow domyslnych
    SOUNDS["shoot"].set_volume(default_volume_shoot)
    SOUNDS["explosion"].set_volume(default_volume_explosion)
    SOUNDS["hit"].set_volume(default_volume_hit)
    SOUNDS["wave"].set_volume(default_volume_wave)
    SOUNDS["healthpack"].set_volume(default_volume_healthpack)
    SOUNDS["player_hurt"].set_volume(default_volume_player_hurt)
    SOUNDS["game_over"].set_volume(default_volume_game_over)

    # Ustawienie glosnosci muzyki w tle
    pygame.mixer.music.set_volume(default_volume_music)