
from scenes.screens.game.GameOverWinScreen import GameOverWinScreen
from scenes.screens.game.GameOverScreen import GameOverScreen
from scenes.screens.game.GameScreen import GameScreen
from scenes.screens.GunScreen import GunScreen
from scenes.screens.MainMenuScreen import MainMenuScreen
from scenes.screens.SettingsScreen import  SettingsScreen
from scenes.screens.GameScreenCharacter import GameScreenCharacter

__screens__ = {
    "MainMenuScreen": MainMenuScreen,
    "GameScreen": GameScreen,
    "GameOverScreen": GameOverScreen,
    "GameOverWinScreen": GameOverWinScreen,
    "GunScreen": GunScreen,
    "SettingsScreen": SettingsScreen,
    "GameScreenCharacter": GameScreenCharacter
}


class SceneHub:

    scene = None

    def __init__(self, screen):
        self.screen = screen

    @property
    def current_scene(self):
        return self.scene

    @current_scene.setter
    def current_scene(self, value):
        self.scene = __screens__[value](self.screen, self)
