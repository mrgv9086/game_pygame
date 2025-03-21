import pygame

from Sprites.viewEntities.Button import Button
from config import Config
from assets.assets import GREEN, BUTTON_GRAY, FON_MAIN_MENU


class GameScreenCharacter:

    def __init__(self, screen, scene_hub):
        # Создание кнопок
        self.menu_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 - 100, 300, 50, "Go menu", BUTTON_GRAY, GREEN)
        self.screen = screen
        self.scene_hub = scene_hub
        self.main_fon = pygame.image.load(FON_MAIN_MENU).convert()

    def update(self):
        self.menu_button.update()

    def draw(self):
        self.image = self.main_fon
        self.screen.blit(self.image, (0, -50))
        self.menu_button.draw(self.screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.is_clicked():
                self.scene_hub.current_scene = "MainMenuScreen"
