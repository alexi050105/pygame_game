# Plik: Imports.py
import random
import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple

# Importujemy wszystkie parametry domyślne
from Parameters.DefaultParameters import *

# Deklarujemy globalne słowniki na grafiki
PLAYER_SPRITES = {}
ENEMY_SPRITES = {}
BULLET_SPRITES = {}


def load_all_game_images() -> None:
    global PLAYER_SPRITES, ENEMY_SPRITES, BULLET_SPRITES

    # 1. Gracz
    raw_p_left = pygame.image.load("graphics/player_left.png").convert_alpha()
    raw_p_right = pygame.image.load("graphics/player_right.png").convert_alpha()
    PLAYER_SPRITES["left"] = pygame.transform.smoothscale(raw_p_left, (50, 50))
    PLAYER_SPRITES["right"] = pygame.transform.smoothscale(raw_p_right, (50, 50))

    # 2. Przeciwnik
    raw_e_left = pygame.image.load("graphics/enemy_left.png").convert_alpha()
    raw_e_right = pygame.image.load("graphics/enemy_right.png").convert_alpha()
    ENEMY_SPRITES["left"] = pygame.transform.smoothscale(raw_e_left, (50, 50))
    ENEMY_SPRITES["right"] = pygame.transform.smoothscale(raw_e_right, (50, 50))

    # 3. Pocisk
    raw_b_left = pygame.image.load("graphics/bullet_left.png").convert_alpha()
    raw_b_right = pygame.image.load("graphics/bullet_right.png").convert_alpha()
    BULLET_SPRITES["left"] = pygame.transform.smoothscale(raw_b_left, (15, 5))
    BULLET_SPRITES["right"] = pygame.transform.smoothscale(raw_b_right, (15, 5))