import os
from config import Config

# Настройки картинок
PLAYER_LEFT_IMG = os.path.join(Config.img_folder, 'player_left.png')
PLAYER_RIGHT_IMG = os.path.join(Config.img_folder, 'player_right.png')
FON_MAIN_MENU = os.path.join(Config.img_folder, 'fon_main_menu.gif')

# Настройки цветов
BLACK = (0, 0, 0)
BACKGROUND = (0, 100, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BACKGROUND_GRAY = (112, 112, 112)
BUTTON_GRAY = (69, 69, 69)
WHITE = (255, 255, 255)

BUTTON_TEXT_COLOR = (31, 206, 203)

GUNCOLOR = (0, 247, 255)
BULLETCOLOR = (255, 255, 0)
RED_MOB_COLOR = (255, 0, 0)
BLUE_MOB_COLOR = (0, 0, 100)
BOSS_COLOR = (200, 50, 100)



TILE_SIZE = 30  # Размер одного тайла
GRID_WIDTH = Config.X_SCREEN * 4 // TILE_SIZE  # Ширина сетки в тайлах
GRID_HEIGHT = Config.Y_SCREEN * 4 // TILE_SIZE  # Высота сетки в тайлах

