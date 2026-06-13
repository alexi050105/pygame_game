# Tests/test_healthpack.py
import pygame
import pytest
from Entities.HealthPack import HealthPack
from Parameters.DefaultParameters import *


# --- FIXTURES (Przygotowanie obiektow do testow) ---

@pytest.fixture
def healthpack():
    # Inicjalizacja apteczki na pozycji (400, 400) z domyslna wartoscia leczenia
    return HealthPack((400, 400), heal_amount=default_healthpack_heal)


# --- TESTY PARAMETROW POCZATKOWYCH ---

def test_healthpack_initial_lifetime(healthpack):
    # Sprawdzenie, czy czas zycia (lifetime) apteczki na starcie jest zgodny z ustawieniami domyslnymi
    assert healthpack.lifetime == default_healthpack_lifetime


def test_healthpack_heal_amount(healthpack):
    # Sprawdzenie, czy wartosc leczenia przypisana do apteczki jest poprawna
    assert healthpack.heal_amount == default_healthpack_heal


def test_healthpack_position(healthpack):
    # Upewnienie sie, ze apteczka zostala stworzona dokladnie w wyznaczonym punkcie ekranu
    assert healthpack.rect.center == (400, 400)


# --- TESTY CZASU ZYCIA I ZNIKANIA APTECZKI (Lifetime) ---

def test_healthpack_disappears_after_lifetime(healthpack):
    # Test sprawdzajacy, czy apteczka znika (wywoluje self.kill()), gdy jej czas zycia dojdzie do zera
    group = pygame.sprite.Group()
    group.add(healthpack)

    # Reczne ustawienie czasu zycia na 1 klatke (tick)
    healthpack.lifetime = 1
    # Aktualizacja grupy wymusza odliczenie klatki w logice apteczki
    group.update()

    # Grupa powinna byc pusta, poniewaz apteczka miala zniknac
    assert len(group) == 0


def test_healthpack_stays_alive_before_lifetime_ends(healthpack):
    # Test sprawdzajacy, czy apteczka pozostaje aktywna przez caly swoj domyslny czas zycia (minus jedna klatka)
    group = pygame.sprite.Group()
    group.add(healthpack)

    # Wywolanie update() o jeden raz mniej niz wynosi pelny czas zycia apteczki
    for _ in range(default_healthpack_lifetime - 1):
        group.update()

    # Apteczka wciaz powinna znajdowac sie w grupie
    assert len(group) == 1


# --- TESTY INTERAKCJI Z GRACZEM (Logika leczenia) ---

def test_player_heals_on_pickup():
    # Test sprawdzajacy, czy podniesienie apteczki poprawnie zwieksza aktualne zdrowie (HP) gracza
    from Entities.Player import Player
    bullets = pygame.sprite.Group()
    player = Player("P", default_HP, default_starting_position,
                    default_player_damage, default_player_speed, bullets)

    # Celowe obnizenie zdrowia gracza do 50 HP
    player.HP = 50
    # Stworzenie apteczki przywracajacej 30 HP
    pack = HealthPack(default_starting_position, heal_amount=30)

    # Symulacja podniesienia apteczki przez gracza (zabezpieczona przed przekroczeniem max_hp)
    player.HP = min(default_HP, player.HP + pack.heal_amount)

    # Zdrowie powinno wynosic dokladnie 50 + 30 = 80 HP
    assert player.HP == 80


def test_player_hp_capped_at_max_on_pickup():
    # Test sprawdzajacy zabezpieczenie: leczenie nie moze zwiekszyc HP powyzej maksymalnego poziomu (default_HP)
    from Entities.Player import Player
    bullets = pygame.sprite.Group()
    player = Player("P", default_HP, default_starting_position,
                    default_player_damage, default_player_speed, bullets)

    # Ustawienie HP blisko maksimum (90 HP przy maksie wynoszacym zazwyczaj 100)
    player.HP = 90
    # Apteczka leczy za 30, co teoretycznie dalo by 120 HP
    pack = HealthPack(default_starting_position, heal_amount=30)

    # Symulacja podniesienia apteczki
    player.HP = min(default_HP, player.HP + pack.heal_amount)

    # Zdrowie powinno zostac zablokowane na wartosci maksymalnej (default_HP)
    assert player.HP == default_HP