# Pygame Game

Gra akcji 2D stworzona w pygame z wykorzystaniem wzorcow projektowych Stan i Dekorator.

## Wymagania lokalne
- Python 3.11
- pygame 2.6.1

## Uruchomienie lokalne
pip install pygame
python main.py

## Sterowanie
- WASD - ruch gracza
- Strzalki - strzelanie w danym kierunku
- ESC - menu / pauza

## Mechaniki
- System fal z rosnacym poziomem trudnosci
- Przeciwnicy: podstawowy, szybki (FastEnemy), opancerzony (ArmoredEnemy)
- Apteczki pojawiajace sie losowo na mapie
- Wzorzec Stan: MenuState, GameplayState, WaveTransitionState, GameOverState
- Wzorzec Dekorator: FastEnemy, ArmoredEnemy

## Uruchomienie przez Docker

### Linux / Debian (zalecane)
sudo apt-get install -y docker.io git
sudo systemctl start docker
sudo usermod -aG docker $USER

Wyloguj sie i zaloguj ponownie, nastepnie:

git clone https://github.com/alexi050105/pygame_game.git
cd pygame_game
docker build -t pygame_game .
xhost +local:docker
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix pygame_game

### Problemy z dzwiekiem na Linux / Debian

Jesli wystapi blad z mixerem audio, zainstaluj pulseaudio i uruchom:

sudo apt-get install -y libasound2-dev pulseaudio
pulseaudio --start
SDL_AUDIODRIVER=pulseaudio python3 main.py

Lub jesli dzwiek nie jest potrzebny:

SDL_AUDIODRIVER=dummy python3 main.py

### Windows
1. Pobierz i zainstaluj Docker Desktop z docker.com/products/docker-desktop
2. Pobierz i uruchom VcXsrv z opcja "Disable access control"
3. Uruchom w PowerShell:

git clone https://github.com/alexi050105/pygame_game.git
cd pygame_game
docker build -t pygame_game .
docker run -e DISPLAY=host.docker.internal:0 -e SDL_AUDIODRIVER=dummy pygame_game

Uwaga: na Windowsie gra moze dzialac wolniej przez X11.
Zalecane uruchomienie na Linuxie lub lokalnie.

## Testy
pytest Tests/ -v