
from screens.GameOverWinScreen import GameOverWinScreen
from screens.GameOverScreen import GameOverScreen
from screens.GameScreen import GameScreen
from screens.GunScreen import GunScreen
from screens.MainMenuScreen import MainMenuScreen
from screens.SettingsScreen import  SettingsScreen
from screens.GameScreenCharacter import GameScreenCharacter

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
