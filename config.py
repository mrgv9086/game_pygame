import os

class Config:

    current_gun = "pistol"

    # Настройка папки игры
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'assets/img')

    # Настройки окна
    X_SCREEN = 1080
    Y_SCREEN = 720
    CAPTION = "I love cats!!!"

    FPS = 60
