# Plik: Imports.py
import random
import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple

# Importujemy wszystkie parametry domyślne
from Parameters.DefaultParameters import *

# Deklarujemy globalne słowniki na grafiki
PLAYER_SPRITES = {}
BASE_ENEMY_SPRITES = {}
FAST_ENEMY_SPRITES = {}
ARMORED_ENEMY_SPRITES = {}
BULLET_SPRITES = {}

BACKGROUND = None
HEALTHPACK_SPRITE = None
BACKGROUND_MENU = None

SOUNDS = {}
MUSIC_PATH = "sounds/happy_adventure.mp3"

def load_all_game_images() -> None:
    global PLAYER_SPRITES, \
        BASE_ENEMY_SPRITES,\
        FAST_ENEMY_SPRITES,\
        ARMORED_ENEMY_SPRITES,\
        BULLET_SPRITES, BACKGROUND, HEALTHPACK_SPRITE, BACKGROUND_MENU

    raw_menu = pygame.image.load("graphics/menu.png").convert()
    BACKGROUND_MENU = pygame.transform.scale(raw_menu, (default_width, default_height))

    enemy_size = (64,41)

    raw_hp = pygame.image.load("graphics/burger.png").convert_alpha()
    HEALTHPACK_SPRITE = pygame.transform.scale(raw_hp, (32, 32))

    raw_bg = pygame.image.load("graphics/map.png").convert()
    BACKGROUND = pygame.transform.smoothscale(raw_bg, (default_width, default_height))

    # 1. Gracz
    raw_p_left = pygame.image.load("graphics/player_left.png").convert_alpha()
    raw_p_right = pygame.image.load("graphics/player_right.png").convert_alpha()
    PLAYER_SPRITES["left"] = pygame.transform.scale(raw_p_left, (46, 76))
    PLAYER_SPRITES["right"] = pygame.transform.scale(raw_p_right, (46, 76))

    # 2. Przeciwnik podstawowy
    raw_b_e_left = pygame.image.load("graphics/default_enemy_left.png").convert_alpha()
    raw_b_e_right = pygame.image.load("graphics/default_enemy_right.png").convert_alpha()
    BASE_ENEMY_SPRITES["left"] = pygame.transform.scale(raw_b_e_left, enemy_size)
    BASE_ENEMY_SPRITES["right"] = pygame.transform.scale(raw_b_e_right, enemy_size)

    raw_f_e_left = pygame.image.load("graphics/fast_enemy_left.png").convert_alpha()
    raw_f_e_right = pygame.image.load("graphics/fast_enemy_right.png").convert_alpha()
    FAST_ENEMY_SPRITES["left"] = pygame.transform.scale(raw_f_e_left, enemy_size)
    FAST_ENEMY_SPRITES["right"] = pygame.transform.scale(raw_f_e_right, enemy_size)

    raw_ar_e_left = pygame.image.load("graphics/armored_enemy_left.png").convert_alpha()
    raw_ar_e_right = pygame.image.load("graphics/armored_enemy_right.png").convert_alpha()
    ARMORED_ENEMY_SPRITES["left"] = pygame.transform.scale(raw_ar_e_left, enemy_size)
    ARMORED_ENEMY_SPRITES["right"] = pygame.transform.scale(raw_ar_e_right, enemy_size)

    # 3. Pocisk
    raw_b_left = pygame.image.load("graphics/bullet_left.png").convert_alpha()
    raw_b_right = pygame.image.load("graphics/bullet_right.png").convert_alpha()
    BULLET_SPRITES["left"] = pygame.transform.smoothscale(raw_b_left, (15, 5))
    BULLET_SPRITES["right"] = pygame.transform.smoothscale(raw_b_right, (15, 5))

def load_all_game_sounds() -> None:
    global SOUNDS
    SOUNDS["shoot"] = pygame.mixer.Sound("sounds/click.wav")
    SOUNDS["explosion"] = pygame.mixer.Sound("sounds/explosion.wav")
    SOUNDS["hit"] = pygame.mixer.Sound("sounds/hitHurt.wav")
    SOUNDS["wave"] = pygame.mixer.Sound("sounds/jump.wav")
    SOUNDS["healthpack"] = pygame.mixer.Sound("sounds/powerUp.wav")
    SOUNDS["player_hurt"] = pygame.mixer.Sound("sounds/playerHurt.wav")
    SOUNDS["game_over"] = pygame.mixer.Sound("sounds/gameOver.wav")


    # Głośność 0.0 - 1.0
    SOUNDS["shoot"].set_volume(default_volume_shoot)
    SOUNDS["explosion"].set_volume(default_volume_explosion)
    SOUNDS["hit"].set_volume(default_volume_hit)
    SOUNDS["wave"].set_volume(default_volume_wave)
    SOUNDS["healthpack"].set_volume(default_volume_healthpack)
    SOUNDS["player_hurt"].set_volume(default_volume_player_hurt)
    SOUNDS["game_over"].set_volume(default_volume_game_over)
    pygame.mixer.music.set_volume(default_volume_music)