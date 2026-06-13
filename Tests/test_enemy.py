# Tests/test_enemy.py
import pygame
import pytest
from Entities.Player import Player
from Entities.Enemy.Enemy import Enemy
from Parameters.DefaultParameters import *

# --- FIXTURES (Przygotowanie obiektow do testow) ---

@pytest.fixture
def player():
    # Inicjalizacja obiektu gracza potzebnego jako cel dla przeciwnika
    return Player("P", default_HP, default_starting_position,
                  default_player_damage, default_player_speed,
                  pygame.sprite.Group())

@pytest.fixture
def enemy(player):
    # Inicjalizacja podstawowego przeciwnika sledzacego powyższego gracza
    return Enemy("E", default_HP, (100, 100),
                 default_damage, default_enemy_speed, player)


# --- TESTY PARAMETROW POCZATKOWYCH ---

def test_enemy_initial_hp(enemy):
    # Sprawdzenie, czy poczatkowa ilosc punktow zdrowia (HP) przeciwnika jest poprawna
    assert enemy.HP == default_HP


# --- TESTY RUCHU (Algorytm sledzenia gracza w osiach X i Y) ---

def test_enemy_moves_right_toward_player(enemy, player):
    # Gracz jest po prawej stronie (300 > 100) -> przeciwnik powinien isc w prawo
    player.rect.centerx = 300
    enemy.rect.centerx = 100
    before = enemy.rect.centerx
    enemy.move_x()
    assert enemy.rect.centerx > before

def test_enemy_moves_left_toward_player(enemy, player):
    # Gracz jest po lewej stronie (50 < 200) -> przeciwnik powinien isc w lewo
    player.rect.centerx = 50
    enemy.rect.centerx = 200
    before = enemy.rect.centerx
    enemy.move_x()
    assert enemy.rect.centerx < before

def test_enemy_moves_down_toward_player(enemy, player):
    # Gracz jest ponizej (300 > 100) -> przeciwnik powinien isc w dol
    player.rect.centery = 300
    enemy.rect.centery = 100
    before = enemy.rect.centery
    enemy.move_y()
    assert enemy.rect.centery > before

def test_enemy_moves_up_toward_player(enemy, player):
    # Gracz jest powyzej (50 < 200) -> przeciwnik powinien isc w gore
    player.rect.centery = 50
    enemy.rect.centery = 200
    before = enemy.rect.centery
    enemy.move_y()
    assert enemy.rect.centery < before


# --- TESTY STRONY, W KTORA OBROCONY JEST PRZECIWNIK (Facing) ---

def test_enemy_facing_right_when_player_is_right(enemy, player):
    # Ustawienie gracza po prawej stronie od przeciwnika
    player.rect.centerx = enemy.rect.centerx + 100
    enemy.update()
    # Przeciwnik powinien obrocic sie w prawo (facing_right = True)
    assert enemy.facing_right is True

def test_enemy_facing_left_when_player_is_left(enemy, player):
    # Ustawienie przeciwnika po prawej, a gracza wyraznie po lewej stronie
    enemy.rect.centerx = 400
    player.rect.centerx = 100  # gracz wyraznie po lewej
    player.rect.centery = enemy.rect.centery  # ten sam poziom y
    enemy.update()
    # Przeciwnik powinien obrocic sie w lewo (facing_right = False)
    assert enemy.facing_right is False