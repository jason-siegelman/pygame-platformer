# settings.py

# --- Screen Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Constants ---
GRAVITY = 0.8
FRICTION = 0.9 
ACCELERATION = 1.0
JUMP_STRENGTH = -18
TILE_SIZE = 50

# --- Colors ---
COLOR_WALL = (100, 200, 100)

# --- Asset Paths ---
BASE_CHAR_PATH = 'assets/kenney_new-platformer-pack-1.1/Sprites/Characters/Default/'
BASE_TILE_PATH = 'assets/kenney_new-platformer-pack-1.1/Sprites/Tiles/Default/'
BASE_ENEMY_PATH = 'assets/kenney_new-platformer-pack-1.1/Sprites/Enemies/Default/'

# --- Level Design ---
# Each character represents a 50x50 tile
# 16 rows x 48 columns
LEVEL_MAP = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                              W",
    "W                                              W",
    "W                             C                W",
    "W       C                     C                W",
    "W      WWW                    C                W",
    "W             P              WWW               W",
    "W            WWW                               W",
    "W                                              W",
    "W      W            C     W          W         W",
    "W     WW           WWW    WW    E   WW         W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]