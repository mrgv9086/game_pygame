import pygame

from Sprites.viewEntities.Button import Button
from assets.assets import GREEN, BUTTON_GRAY, BACKGROUND_GRAY
from config import Config


class GunScreen:

    def __init__(self, screen, scene_hub):
        # Создание кнопок
        self.menu_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 - 100, 300, 50, "Go menu", BUTTON_GRAY, GREEN)
        self.pistol_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2, 300, 50, "pistol", BUTTON_GRAY, GREEN)
        self.backshoot_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 + 100, 300, 50, "backshoot", BUTTON_GRAY, GREEN)
        self.screen = screen
        self.scene_hub = scene_hub

    def update(self):
        self.menu_button.update()
        self.pistol_button.update()
        self.backshoot_button.update()

    def draw(self):
        self.screen.fill(BACKGROUND_GRAY)
        self.menu_button.draw(self.screen)
        self.pistol_button.draw(self.screen)
        self.backshoot_button.draw(self.screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.is_clicked():
                self.scene_hub.current_scene = "MainMenuScreen"
            if self.pistol_button.is_clicked():
                Config.current_gun = "pistol"
            elif self.backshoot_button.is_clicked():
                Config.current_gun = "backshoot"
