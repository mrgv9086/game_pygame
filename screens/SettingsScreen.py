import pygame

from Sprites.Button import Button
from config import X_SCREEN, Y_SCREEN
from assets import GREEN, BUTTON_GRAY, BACKGROUND_GRAY


class SettingsScreen:

    def __init__(self, screen, scene_hub):
        # Создание кнопок
        self.menu_button = Button(X_SCREEN // 2 - 150, Y_SCREEN // 2 - 100, 300, 50, "Go menu", BUTTON_GRAY, GREEN)
        self.screen = screen
        self.scene_hub = scene_hub

    def update(self):
        self.menu_button.update()

    def draw(self):
        self.screen.fill(BACKGROUND_GRAY)
        self.menu_button.draw(self.screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.is_clicked():
                self.scene_hub.current_scene = "MainMenuScreen"
