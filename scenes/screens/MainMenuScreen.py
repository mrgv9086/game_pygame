import pygame

from Sprites.viewEntities.Button import Button
from config import Config
from assets.assets import GREEN, BUTTON_GRAY, BACKGROUND_GRAY


class MainMenuScreen:

    def __init__(self, screen, scene_hub):
        # Создание кнопок
        self.play_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 - 150, 300, 50, "Start", BUTTON_GRAY, GREEN)
        self.settings_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 - 50, 300, 50, "Настройки", BUTTON_GRAY, GREEN)
        self.character_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 + 50, 300, 50, "Персонаж", BUTTON_GRAY, GREEN)
        self.weapon_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 + 150, 300, 50, "Оружие", BUTTON_GRAY, GREEN)
        self.exit_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 + 250, 300, 50, "Выход", BUTTON_GRAY, GREEN)
        self.screen = screen
        self.scene_hub = scene_hub

    def update(self):
        self.play_button.update()
        self.settings_button.update()
        self.character_button.update()
        self.weapon_button.update()
        self.exit_button.update()

    def draw(self):
        self.screen.fill(BACKGROUND_GRAY)
        self.play_button.draw(self.screen)
        self.settings_button.draw(self.screen)
        self.weapon_button.draw(self.screen)
        self.character_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.is_clicked():
                self.scene_hub.current_scene = "GameScreen"
            if self.weapon_button.is_clicked():
                self.scene_hub.current_scene = "GunScreen"
            if self.settings_button.is_clicked():
                self.scene_hub.current_scene = "SettingsScreen"
            if self.character_button.is_clicked():
                self.scene_hub.current_scene = "GameScreenCharacter"
            if self.exit_button.is_clicked():
                pygame.quit()
