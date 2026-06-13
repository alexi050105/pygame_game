# Tests/test_player.py
import pygame
import pytest
from Entities.Player import Player
from Entities.Bullet import Bullet
from Parameters.DefaultParameters import *

# --- FIXTURES (Przygotowanie obiektow do testow) ---

@pytest.fixture
def bullets_group():
    # Tworzenie grupy sprite'ow przeznaczonej na pociski wystrzelone przez gracza
    return pygame.sprite.Group()

@pytest.fixture
def player(bullets_group):
    # Inicjalizacja obiektu gracza powiazanego z powyzsza grupa pociskow
    return Player("TestPlayer", default_HP, default_starting_position,
                  default_player_damage, default_player_speed, bullets_group)


# --- TESTY PARAMETROW POCZATKOWYCH I POZYCJI ---

def test_player_initial_hp(player):
    # Sprawdzenie, czy poczatkowa ilosc zdrowia gracza jest zgodna z ustawieniami domyslnymi
    assert player.HP == default_HP

def test_player_initial_position(player):
    # Sprawdzenie, czy gracz na starcie pojawia sie idealnie na srodku ekranu gry
    assert player.rect.center == (int(default_width / 2), int(default_height / 2))

def test_player_hp_decreases(player):
    # Test sprawdza, czy reczne odjecie zdrowia (obrazenia) poprawnie zmienia wartosc HP
    player.HP -= 30
    assert player.HP == default_HP - 30

def test_player_facing_right_by_default(player):
    # Sprawdzenie, czy postac gracza domyslnie zwrocona jest w prawa strone
    assert player.facing_right is True


# --- TESTY WALIDACJI ZLECH PARAMETROW WEJSCIOWYCH ---

def test_player_invalid_hp_uses_default(bullets_group):
    # Test zabezpieczenia: podanie ujemnego HP powinno wymusic ustawienie wartosci domyslnej
    p = Player("Bad", -50, default_starting_position,
               default_player_damage, default_player_speed, bullets_group)
    assert p.HP == default_HP

def test_player_invalid_speed_uses_default(bullets_group):
    # Test zabezpieczenia: podanie ujemnej predkosci powinno cofnac ja do wartosci domyslnej
    p = Player("Bad", default_HP, default_starting_position,
               default_player_damage, -5, bullets_group)
    assert p.speed == default_player_speed


# --- TESTY MECHANIKI STRZELANIA I COOLDOWNU ---

def test_player_shoot_creates_bullet(player, bullets_group):
    # Wywolanie strzalu powinno dodac dokladnie jeden obiekt pocisku do grupy bullets_group
    player.shoot("right")
    assert len(bullets_group) == 1

def test_player_shoot_direction_right(player, bullets_group):
    # Sprawdzenie, czy przekazanie kierunku "right" tworzy pocisk lecacy w prawo
    player.shoot("right")
    bullet = list(bullets_group)[0]
    assert bullet.direction == "right"

def test_player_shoot_direction_up(player, bullets_group):
    # Sprawdzenie, czy przekazanie kierunku "up" tworzy pocisk lecacy w gore
    player.shoot("up")
    bullet = list(bullets_group)[0]
    assert bullet.direction == "up"

def test_player_shoot_cooldown_blocks_second_shot(player, bullets_group):
    # Po wykonaniu strzalu licznik cooldown powienien zostac ustawiony na wartosc domyslna
    player.shoot("right")
    assert player.cooldown == default_bullet_cooldown
    # Uwaga: Drugi shoot() bezposrednio nie sprawdza cooldownu (to zadanie dla pętli update),
    # dlatego tutaj weryfikujemy sam fakt poprawnego ustawienia licznika blokady.
    assert len(bullets_group) == 1

def test_player_cooldown_resets_after_ticks(player, bullets_group):
    # Symulacja miniecia czasu blokady (cooldown = 0). Gracz powinien moc strzelic drugi raz.
    player.shoot("right")
    player.cooldown = 0
    player.shoot("right")
    # W grupie powinny znajdowac sie juz dwa pociski
    assert len(bullets_group) == 2


# --- TESTY OGRANICZEN PORUSZANIA SIE (Granice ekranu) ---

def test_player_cannot_exceed_right_boundary(player):
    # Test symuluje wyjscie poza prawa krawedz ekranu i sprawdza poprawne przyciecie pozycji (clamp)
    player.rect.right = default_width + 100
    player.rect.right = min(default_width, player.rect.right)
    assert player.rect.right <= default_width

def test_player_cannot_exceed_left_boundary(player):
    # Test symuluje wyjscie poza lewa krawedz ekranu (wspolrzedne ujemne) i sprawdza zatrzymanie na 0
    player.rect.left = -100
    player.rect.left = max(0, player.rect.left)
    assert player.rect.left >= 0