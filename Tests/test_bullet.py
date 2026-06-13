# Tests/test_bullet.py
import pygame
import pytest
from Entities.Bullet import Bullet
from Parameters.DefaultParameters import *

# --- FIXTURES (Przygotowanie obiektow testowych) ---

# Tworzenie pocisku poruszajacego sie w prawo na pozycji (400, 400)
@pytest.fixture
def bullet_right():
    return Bullet(default_player_damage, default_bullet_speed, (400, 400), "right")

# Tworzenie pocisku poruszajacego sie w lewo na pozycji (400, 400)
@pytest.fixture
def bullet_left():
    return Bullet(default_player_damage, default_bullet_speed, (400, 400), "left")

# Tworzenie pocisku poruszajacego sie w gore na pozycji (400, 400)
@pytest.fixture
def bullet_up():
    return Bullet(default_player_damage, default_bullet_speed, (400, 400), "up")

# Tworzenie pocisku poruszajacego sie w dol na pozycji (400, 400)
@pytest.fixture
def bullet_down():
    return Bullet(default_player_damage, default_bullet_speed, (400, 400), "down")


# --- TESTY PORUSZANIA SIE (Ruch w osiach X i Y) ---

def test_bullet_moves_right(bullet_right):
    # Sprawdzenie, czy pocisk skierowany w prawo zwieksza swoja wspolrzedna X po aktualizacji
    x_before = bullet_right.rect.x
    bullet_right.update()
    assert bullet_right.rect.x > x_before

def test_bullet_moves_left(bullet_left):
    # Sprawdzenie, czy pocisk skierowany w lewo zmniejsza swoja wspolrzedna X po aktualizacji
    x_before = bullet_left.rect.x
    bullet_left.update()
    assert bullet_left.rect.x < x_before

def test_bullet_moves_up(bullet_up):
    # Sprawdzenie, czy pocisk skierowany w gore zmniejsza swoja wspolrzedna Y (w Pygame gora to mniejsze Y)
    y_before = bullet_up.rect.y
    bullet_up.update()
    assert bullet_up.rect.y < y_before

def test_bullet_moves_down(bullet_down):
    # Sprawdzenie, czy pocisk skierowany w dol zwieksza swoja wspolrzedna Y po aktualizacji
    y_before = bullet_down.rect.y
    bullet_down.update()
    assert bullet_down.rect.y > y_before


# --- TESTY WALIDACJI PARAMETROW WEJSCIOWYCH ---

def test_bullet_invalid_damage_uses_default():
    # Test zabezpieczenia: podanie ujemnych obrazen powinno ustawic domyslna wartosc (default_damage)
    b = Bullet(-10, default_bullet_speed, (400, 400), "right")
    assert b.damage == default_damage

def test_bullet_invalid_speed_uses_default():
    # Test zabezpieczenia: podanie ujemnej predkosci powinno ustawic domyslna predkosc pocisku
    b = Bullet(default_player_damage, -5, (400, 400), "right")
    assert b.speed == default_bullet_speed


# --- TESTY USUWANIA POCISKU POZA EKRANEM (Out of Bounds) ---

def test_bullet_killed_when_out_of_bounds_right():
    # Test sprawdzajacy, czy pocisk lecacy w prawo zostanie usuniety z grupy po przekroczeniu granicy ekranu
    group = pygame.sprite.Group()
    # Ustawienie pozycji startowej pocisku celowo poza prawa krawedzia ekranu
    b = Bullet(default_player_damage, default_bullet_speed,
               (default_width + default_out_of_bounds, 400), "right")
    group.add(b)
    b.update()
    # Po wywolaniu update(), pocisk powinien wykryc, ze jest poza ekranem i wykonac self.kill()
    assert len(group) == 0

def test_bullet_killed_when_out_of_bounds_up():
    # Test sprawdzajacy, czy pocisk lecacy w gore zostanie usuniety po przekroczeniu gornej granicy ekranu
    group = pygame.sprite.Group()
    # Ustawienie pozycji startowej pocisku celowo powyzej gornej krawedzi ekranu (wartosc ujemna)
    b = Bullet(default_player_damage, default_bullet_speed,
               (400, -default_out_of_bounds), "up")
    group.add(b)
    b.update()
    # Po wywolaniu update(), pocisk powinien zniknac z grupy sprite'ow
    assert len(group) == 0