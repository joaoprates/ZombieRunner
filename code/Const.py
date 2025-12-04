"""
Constantes e configurações globais do jogo.
"""

# Dimensões da tela
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

# FPS
FPS = 60

# Título da janela
WINDOW_TITLE = "Zombie Runner - Trabalho Pratico"

# Cores (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Estados do jogo
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_GAME_WIN = "game_win"
STATE_PAUSED = "paused"

# Caminhos de assets
ASSET_DIR = "asset"

PLAYER_IMG = f"{ASSET_DIR}/player.png"
ZOMBIE_IMG = f"{ASSET_DIR}/zombie.png"
BULLET_IMG = f"{ASSET_DIR}/bullet.png"
BACKGROUND_IMG = f"{ASSET_DIR}/game_background.png"
MENU_BACKGROUND_IMG = f"{ASSET_DIR}/menu_background.png"
HEART_IMG = f"{ASSET_DIR}/heart.png"

FONT_FILE = f"{ASSET_DIR}/ZOMBIE.ttf"
SHOOT_SOUND_FILE = f"{ASSET_DIR}/shoot.wav"
HIT_SOUND_FILE = f"{ASSET_DIR}/hit.wav"
MUSIC_FILE = f"{ASSET_DIR}/music.wav"

# Configuração de jogo
INITIAL_LIVES = 3
POINTS_PER_ZOMBIE = 10
