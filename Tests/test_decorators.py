# Tests/test_decorators.py
import pygame
import pytest
from Entities.Player import Player
from Entities.Enemy.FastEnemy import FastEnemy
from Entities.Enemy.ArmoredEnemy import ArmoredEnemy
from Entities.Enemy.Enemy import Enemy
from Parameters.DefaultParameters import *

# --- FIXTURES (Przygotowanie obiektow do testow) ---

@pytest.fixture
def player():
    # Tworzenie instancji gracza z domyslnymi parametrami i pusta grupa pociskow
    return Player("P", default_HP, default_starting_position,
                  default_player_damage, default_player_speed,
                  pygame.sprite.Group())

@pytest.fixture
def base_enemy(player):
    # Tworzenie podstawowego przeciwnika, ktory sledzi pozycje gracza
    return Enemy("E", default_HP, (100, 100),
                 default_damage, default_enemy_speed, player)


# --- TESTY DLA FAST_ENEMY (Szybki Przeciwnik) ---

def test_fast_enemy_moves_faster_than_base(base_enemy, player):
    # Ustawienie pozycji gracza po prawej stronie, aby wymusic ruch przeciwnika w prawo
    player.rect.centerx = 300
    base_x = base_enemy.rect.centerx

    import copy
    # Tworzenie kopii zapasowej podstawowego przeciwnika do porownania dystansu
    base_copy = copy.copy(base_enemy)
    base_copy.rect = base_enemy.rect.copy()

    # Opakowanie podstawowego przeciwnika w dekorator FastEnemy ze zvielokrotniona predkoscia (x2.0)
    fast = FastEnemy(base_enemy, multiplier=2.0)
    fast.rect.centerx = base_x
    fast._wrapped.rect.centerx = base_x

    # Wykonanie ruchu w osi X
    fast.move_x()
    # Sprawdzenie, czy udekorowany (szybki) przeciwnik pokonal wiekszy dystans niz domyslna predkosc bazowa
    assert fast.rect.centerx > base_x + default_enemy_speed

def test_fast_enemy_delegates_attributes(base_enemy):
    # Test sprawdza, czy dekorator poprawnie przekazuje (deleguje) pobieranie atrybutow z obiektu bazowego
    fast = FastEnemy(base_enemy)
    assert fast.HP == default_HP
    assert fast.damage == default_damage


# --- TESTY DLA ARMORED_ENEMY (Opancerzony Przeciwnik) ---

def test_armored_enemy_survives_first_hit(base_enemy):
    # Opancerzony przeciwnik powinien przezyc pierwsze trafienie dzieki pancerzowi (take_hit zwraca False, bo nie zginal)
    armored = ArmoredEnemy(base_enemy)
    assert armored.take_hit() is False

def test_armored_enemy_dies_on_second_hit(base_enemy):
    # Opancerzony przeciwnik powinien zginac przy drugim trafieniu (take_hit zwraca True)
    armored = ArmoredEnemy(base_enemy)
    armored.take_hit()  # Pierwsze trafienie niszczy pancerz
    assert armored.take_hit() is True  # Drugie trafienie zabija przeciwnika

def test_armored_enemy_initial_hits(base_enemy):
    # Sprawdzenie, czy ilosc punktow pancerza na starcie jest zgodna z domyslnymi parametrami
    armored = ArmoredEnemy(base_enemy)
    assert armored.hits_remaining == default_armored_enemy_hits


# --- TESTY DLA ZLOZONYCH DEKORATOROW (Stackowanie efektow) ---

def test_stacked_decorators_armored_then_fast(base_enemy):
    # Test laczenia dekoratorow: stworzenie przeciwnika, ktory jest JEDNOCZESNIE szybki i opancerzony
    enemy = FastEnemy(ArmoredEnemy(base_enemy))
    # Zachowanie pancerza powinno zostac zachowane (pierwszy strzal nic nie robi, drugi zabija)
    assert enemy.take_hit() is False
    assert enemy.take_hit() is True

def test_stacked_decorators_rect_sync(base_enemy, player):
    # Test sprawdzajacy synchronizacje pozycji (rect) w zagniezdzonych dekoratorach
    player.rect.centerx = 300
    enemy = FastEnemy(ArmoredEnemy(base_enemy))
    enemy.move_x()
    # Upewnienie sie, ze zmiana pozycji zewnetrznego dekoratora aktualizuje tez pozycje obiektow opakowanych wewnatrz
    assert enemy.rect == enemy._wrapped.rect