FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install pygame==2.6.1

ENV SDL_VIDEODRIVER=x11
ENV SDL_AUDIODRIVER=dummy

CMD ["python", "main.py"]