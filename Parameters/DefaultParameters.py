# DefaultParameters.py
default_fps = 60
default_font = "fonts/Minecraft.ttf"
default_font_size = 40
default_font_size_small = 28
default_font_size_hud = 20
default_HP = 100
default_width = 800
default_height = 800
default_starting_position = (default_width / 2, default_height / 2)
default_out_of_bounds = 100
default_player_damage = 50
default_damage = 10
default_player_speed = 5
default_enemy_speed = 1
default_bullet_speed = 20
default_bullet_cooldown = 20

default_hud_background_width = 220
default_hud_background_height = 80
default_hud_background_alpha = 150

# Limity do regulacji w GameSetupState
min_player_hp = 50
max_player_hp = 200
hp_step = 10

min_starting_enemies = 1
max_starting_enemies = 10
enemies_step = 1

default_music_volume = 0.4
default_sfx_volume = 0.5
default_volume_step = 0.1

# Trudnosc

default_kills_per_enemy_slot = 2  # ile razy trzeba "wymienic" cala grupe wrogow

difficulty_easy_enemies_multiplier = 0.6
difficulty_normal_enemies_multiplier = 1.0
difficulty_hard_enemies_multiplier = 1.6

difficulty_easy_healthpack_multiplier = 1.5   # apteczki czesciej
difficulty_normal_healthpack_multiplier = 1.0
difficulty_hard_healthpack_multiplier = 0.6   # apteczki rzadziej

difficulty_easy_decorator_multiplier = 0.5    # mniej Fast/Armored
difficulty_normal_decorator_multiplier = 1.0
difficulty_hard_decorator_multiplier = 1.8    # wiecej Fast/Armored

min_player_hp = 50
max_player_hp = 200
hp_step = 10

min_starting_enemies = 1
max_starting_enemies = 10
enemies_step = 1

# Fale
default_starting_wave = 1
default_starting_kills = 0
default_starting_enemies_to_kill = 5
default_starting_enemies_max_count = 3
default_wave_kills_increment = 3
default_wave_enemies_increment = 1

# Apteczka
default_healthpack_heal = 30
default_healthpack_lifetime = 300
default_healthpack_interval = 300

# Separacja przeciwnikow
default_separation_iterations = 3
default_separation_divisor = 4

# HUD
default_hud_bar_x = 10
default_hud_bar_y = 40
default_hud_bar_width = 200
default_hud_bar_height = 18

# Dzwieki
default_volume_shoot = 0.3
default_volume_explosion = 0.2
default_volume_hit = 0.3
default_volume_wave = 0.7
default_volume_healthpack = 0.6
default_volume_player_hurt = 0.5
default_volume_game_over = 0.7
default_volume_music = 0.4

# Dekoratory
default_fast_enemy_multiplier = 2.0
default_armored_enemy_hits = 2
default_fast_enemy_chance = 0.3
default_armored_enemy_chance = 0.3
default_fast_enemy_min_wave = 2
default_armored_enemy_min_wave = 3

# Kierunek sprite'a
default_direction_threshold = 20