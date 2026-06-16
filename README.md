# Pygame Game

Gra akcji 2D stworzona w pygame z wykorzystaniem wzorcow projektowych Stan (State) i Dekorator (Decorator). Gracz odpiera kolejne fale przeciwnikow, zbiera apteczki i moze dostosowac poziom trudnosci przed rozpoczeciem rozgrywki.

## Opis projektu

Gracz porusza sie po mapie i strzela do nadchodzacych przeciwnikow. Z kazda kolejna fala przeciwnikow przybywa, a niektorzy z nich otrzymuja dodatkowe wlasciwosci (wiekszą predkosc lub odpornosc na obrazenia) realizowane przez wzorzec Dekorator. Cala logika ekranow gry (menu, rozgrywka, pauza, ustawienia, koniec gry) zarzadzana jest przez wzorzec Stan.

## Instrukcja dla uzytkownika

### Co zrobic po uruchomieniu

Po starcie gry pojawia sie **menu glowne**. Z menu mozna przejsc dwoma sciezkami:

- **ESC** — przechodzi do ekranu ustawien rozgrywki, gdzie nalezy wybrac parametry przed startem
- **TAB** — przechodzi do ustawien dzwieku (mozliwe do zmiany w kazdym momencie, nawet w trakcie gry)

### Ustawienia rozgrywki (przed startem)

Na ekranie ustawien rozgrywki mozna wybrac:

- **Poziom trudnosci** — strzalki lewo/prawo (Easy / Normal / Hard); wplywa na liczbe przeciwnikow na mapie, czestotliwosc apteczek oraz szanse na wystapienie przeciwnikow z dekoratorami
- **Startowe HP gracza** — klawisze W/S
- **Liczba przeciwnikow na starcie** — klawisze A/D

Po ustawieniu parametrow nalezy wcisnac **ENTER**, aby rozpoczac rozgrywke. Po starcie te ustawienia sa zablokowane do konca danej sesji gry.

### Sterowanie w trakcie rozgrywki

- **W A S D** — ruch gracza (gora, lewo, dol, prawo)
- **Strzalki (gora/dol/lewo/prawo)** — strzelanie pociskiem w danym kierunku
- **ESC** — wejscie w pauze (gra zostaje zamrozona, muzyka wstrzymana)
- **F5** — zapis aktualnego stanu gry do pliku
- **F9** — wczytanie ostatnio zapisanego stanu gry

Na ekranie podczas gry widoczny jest panel (HUD) w lewym gornym rogu z paskiem HP oraz numerem aktualnej fali i liczba potrzebnych zabic do jej zakonczenia. W prawym gornym rogu znajduje sie przypomnienie klawiszy zapisu i wczytania gry.

### Pauza

W trakcie pauzy dostepne sa nastepujace opcje:

- **ESC** — powrot do rozgrywki w miejscu, w ktorym zostala przerwana
- **TAB** — przejscie do ustawien dzwieku
- **M** — powrot do menu glownego (powoduje reset calej rozgrywki: HP, fali, przeciwnikow i pozycji gracza)

### Ustawienia dzwieku

Dostepne w kazdym momencie gry (z menu glownego lub z pauzy):

- **Strzalki gora/dol** — regulacja glosnosci muzyki w tle
- **Strzalki lewo/prawo** — regulacja glosnosci efektow dzwiekowych
- **ESC** — powrot do poprzedniego ekranu

### Zapisywanie i wczytywanie danych

Gra umozliwia zapisanie calego stanu rozgrywki do pliku tekstowego `savegame.json`, ktory powstaje w tym samym folderze, z ktorego uruchamiana jest gra (lub plik .exe).

- Wciskajac **F5** w trakcie rozgrywki, zapisywane sa: HP gracza, jego pozycja, numer aktualnej fali, liczba potrzebnych zabic, wszyscy aktualnie zywi przeciwnicy (wraz z ich typem - podstawowy, szybki, opancerzony) oraz wszystkie aktywne apteczki na mapie
- Wciskajac **F9**, cala ta sytuacja zostaje odtworzona — gra wraca do stanu z momentu ostatniego zapisu
- Po wykonaniu zapisu lub wczytania na ekranie pojawia sie krotki komunikat ("ZAPISANO GRE" / "WCZYTANO GRE") informujacy o powodzeniu operacji; w razie braku pliku zapisu pojawi sie komunikat "BRAK ZAPISU"

### Koniec gry

Gra konczy sie, gdy HP gracza spadnie do zera po kontakcie z przeciwnikiem. Na ekranie koncowym wyswietlane sa: numer osiagnietej fali, wybrany poziom trudnosci oraz ustawienia startowe (HP i liczba przeciwnikow). Wciskajac **ESC**, mozna wrocic do menu glownego i rozpoczac nowa rozgrywke.


## Zaleznosci

- Python 3.11
- pygame 2.6.1
- pytest (opcjonalnie, do uruchamiania testow)
- pyinstaller (opcjonalnie, do budowania pliku .exe)
- Docker (opcjonalnie, do uruchomienia w kontenerze)

## Struktura projektu

```
gameProject/
├── Entities/              # Klasy postaci i obiektow gry
│   ├── Person.py          # Klasa bazowa postaci (gracz/przeciwnik)
│   ├── Player.py          # Gracz
│   ├── Bullet.py          # Pocisk
│   ├── HealthPack.py      # Apteczka
│   └── Enemy/
│       ├── Enemy.py            # Podstawowy przeciwnik
│       ├── EnemyDecorator.py   # Bazowy dekorator przeciwnika
│       ├── FastEnemy.py        # Dekorator - szybszy przeciwnik
│       └── ArmoredEnemy.py     # Dekorator - opancerzony przeciwnik
├── States/                # Stany gry (wzorzec Stan)
│   ├── GameState.py            # Abstrakcyjna klasa bazowa stanu
│   ├── MenuState.py            # Menu glowne
│   ├── GameSetupState.py       # Ustawienia rozgrywki (trudnosc, HP, liczba wrogow)
│   ├── SettingsState.py        # Ustawienia dzwieku
│   ├── GameplayState.py        # Glowna rozgrywka
│   ├── PauseState.py           # Pauza
│   ├── WaveTransitionState.py  # Przejscie miedzy falami
│   └── GameOverState.py        # Koniec gry
├── Game/
│   ├── Game.py             # Glowna klasa gry i petla gry
│   └── SaveManager.py      # Zapis i wczytywanie stanu gry
├── Parameters/
│   ├── DefaultParameters.py  # Wszystkie wartosci domyslne i konfiguracyjne
│   └── Imports.py            # Wspolne importy, ladowanie grafik i dzwiekow
├── Tests/                  # Testy jednostkowe (pytest)
├── graphics/                # Pliki graficzne (sprite'y, tla, mapa)
├── sounds/                  # Pliki dzwiekowe i muzyka
├── fonts/                   # Czcionka uzywana w grze
├── main.py                  # Punkt wejscia do programu
├── Dockerfile                # Konfiguracja obrazu Dockerowego
└── .gitignore
```

## Uruchomienie lokalne

```
pip install pygame
python main.py
```

## Uruchomienie przez Docker

### Linux / Debian (zalecane)

```
sudo apt-get install -y docker.io git
sudo systemctl start docker
sudo usermod -aG docker $USER
```

Wyloguj sie i zaloguj ponownie, nastepnie:

```
git clone https://github.com/alexi050105/pygame_game.git
cd pygame_game
docker build -t pygame_game .
xhost +local:docker
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pygame_game
```

#### Problemy z dzwiekiem na Linux / Debian

Jesli wystapi blad z mixerem audio, zainstaluj pulseaudio i uruchom:

```
sudo apt-get install -y libasound2-dev pulseaudio
pulseaudio --start
SDL_AUDIODRIVER=pulseaudio python3 main.py
```

Lub jesli dzwiek nie jest potrzebny:

```
SDL_AUDIODRIVER=dummy python3 main.py
```

### Windows

1. Pobierz i zainstaluj Docker Desktop z docker.com/products/docker-desktop
2. Pobierz i uruchom VcXsrv z opcja "Disable access control"
3. Uruchom w PowerShell:

```
git clone https://github.com/alexi050105/pygame_game.git
cd pygame_game
docker build -t pygame_game .
docker run -e DISPLAY=host.docker.internal:0 -e SDL_AUDIODRIVER=dummy pygame_game
```

Uwaga: na Windowsie gra moze dzialac wolniej przez przesylanie obrazu po sieci X11. Zalecane uruchomienie na Linuxie lub lokalnie.

## Budowanie pliku .exe (Windows)

```
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "graphics;graphics" --add-data "sounds;sounds" --add-data "fonts;fonts" --name "MyGame" main.py
```

Plik wynikowy znajdziesz w folderze `dist/`. Plik .exe jest samodzielny i mozna go przeniesc na inny komputer bez instalowania Pythona.

## Testy

```
pytest Tests/ -v
```

---