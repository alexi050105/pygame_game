import json
import os

SAVE_PATH = "savegame.json"


class SaveManager:
    @staticmethod
    def save_game(manager) -> bool:
        player = manager.player_group.sprite
        if not player:
            return False

        data = {
            "player": {
                "HP": player.HP,
                "position": [player.rect.centerx, player.rect.centery]
            },
            "wave": {
                "current_wave": manager.current_wave,
                "kills_in_wave": manager.kills_in_wave,
                "enemies_to_kill": manager.enemies_to_kill,
                "enemies_max_count": manager.enemies_max_count
            },
            "enemies": [
                {
                    "position": [enemy.rect.centerx, enemy.rect.centery],
                    "HP": enemy.HP,
                    "type": SaveManager.__get_enemy_type(enemy)
                }
                for enemy in manager.enemies_group
            ],
            "healthpacks": [
                {
                    "position": [pack.rect.centerx, pack.rect.centery],
                    "heal_amount": pack.heal_amount,
                    "lifetime": pack.lifetime
                }
                for pack in manager.healthpacks_group
            ]
        }

        try:
            with open(SAVE_PATH, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except IOError:
            return False

    @staticmethod
    def __get_enemy_type(enemy) -> str:
        # Sprawdzamy typy dekoratorow przez isinstance, zaczynajac od najbardziej zewnetrznego
        from Entities.Enemy.FastEnemy import FastEnemy
        from Entities.Enemy.ArmoredEnemy import ArmoredEnemy

        is_fast = isinstance(enemy, FastEnemy)
        is_armored = isinstance(enemy, ArmoredEnemy) or (hasattr(enemy, '_wrapped') and isinstance(enemy._wrapped, ArmoredEnemy))

        if is_fast and is_armored:
            return "fast_armored"
        elif is_fast:
            return "fast"
        elif is_armored:
            return "armored"
        return "base"

    @staticmethod
    def load_game(manager) -> bool:
        if not os.path.exists(SAVE_PATH):
            return False

        try:
            with open(SAVE_PATH, "r") as f:
                data = json.load(f)
        except (IOError, json.JSONDecodeError):
            return False

        from Entities.Enemy.Enemy import Enemy
        from Entities.Enemy.FastEnemy import FastEnemy
        from Entities.Enemy.ArmoredEnemy import ArmoredEnemy
        from Entities.HealthPack import HealthPack
        from Parameters.DefaultParameters import default_damage, default_enemy_speed

        # Wczytanie gracza
        player = manager.player_group.sprite
        if player:
            player.HP = data["player"]["HP"]
            player.rect.center = tuple(data["player"]["position"])

        # Wczytanie postepu fali
        manager.current_wave = data["wave"]["current_wave"]
        manager.kills_in_wave = data["wave"]["kills_in_wave"]
        manager.enemies_to_kill = data["wave"]["enemies_to_kill"]
        manager.enemies_max_count = data["wave"]["enemies_max_count"]

        # Wyczyszczenie obecnych grup
        manager.enemies_group.empty()
        manager.healthpacks_group.empty()

        # Odtworzenie przeciwnikow z odpowiednimi dekoratorami
        for enemy_data in data["enemies"]:
            pos = tuple(enemy_data["position"])
            base = Enemy("Enemy", enemy_data["HP"], pos, default_damage,
                         default_enemy_speed, player)

            enemy_type = enemy_data["type"]
            if enemy_type == "fast":
                enemy = FastEnemy(base)
            elif enemy_type == "armored":
                enemy = ArmoredEnemy(base)
            elif enemy_type == "fast_armored":
                enemy = FastEnemy(ArmoredEnemy(base))
            else:
                enemy = base

            manager.enemies_group.add(enemy)

        # Odtworzenie apteczek
        for pack_data in data["healthpacks"]:
            pos = tuple(pack_data["position"])
            pack = HealthPack(pos, pack_data["heal_amount"])
            pack.lifetime = pack_data["lifetime"]
            manager.healthpacks_group.add(pack)

        return True