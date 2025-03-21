import pygame

from Sprites.viewEntities.Button import Button
from config import Config
from assets.assets import GREEN, BUTTON_GRAY, FON_MAIN_MENU
from DataBase import get_total_time


class SettingsScreen:

    def __init__(self, screen, scene_hub):
        # Создание кнопок
        self.menu_button = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 - 100, 300, 50, "Go menu",
                                  BUTTON_GRAY, GREEN)
        self.volume_up = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 - 200, 300, 50, "v+", BUTTON_GRAY,
                                GREEN)
        self.volume_down = Button(Config.X_SCREEN // 2 - 150, Config.Y_SCREEN // 2 - 250, 300, 50, "v-", BUTTON_GRAY,
                                  GREEN)
        self.screen = screen
        self.scene_hub = scene_hub
        self.total_time_text = None
        self.font = pygame.font.Font(None, 36)  # шрифт для текста
        self.main_fon = pygame.image.load(FON_MAIN_MENU).convert()

        self.text = self.font.render(f"volume:{Config.current_volume}", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(x=Config.X_SCREEN // 2 - 150, y=Config.Y_SCREEN // 2 - 300)

    def update(self):
        self.menu_button.update()
        self.volume_up.update()
        self.volume_down.update()
        total_time_seconds = get_total_time()
        hours = total_time_seconds // 3600
        minutes = (total_time_seconds % 3600) // 60
        seconds = total_time_seconds % 60
        self.total_time_text = self.font.render(f"Total Time: {hours}:{minutes:02}:{seconds:02}", True, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.main_fon, (0, -50))

        self.menu_button.draw(self.screen)
        self.volume_up.draw(self.screen)
        self.volume_down.draw(self.screen)

        if self.total_time_text:
            text_rect = self.total_time_text.get_rect(center=(Config.X_SCREEN // 2, Config.Y_SCREEN // 2))
            self.screen.blit(self.total_time_text, text_rect)

        self.screen.blit(self.text, self.text_rect)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.is_clicked():
                self.scene_hub.current_scene = "MainMenuScreen"
            if self.volume_up.is_clicked():
                Config.current_volume += 10
                if Config.current_volume > 100:
                    Config.current_volume = 100
                Config.fon.set_volume(min(Config.current_volume / 100, 1.0))
                self.text = self.font.render(f"volume:{Config.current_volume}", True, (255, 0, 0))
            if self.volume_down.is_clicked():
                Config.current_volume -= 10
                if Config.current_volume < 0:
                    Config.current_volume = 0
                Config.fon.set_volume(max(Config.current_volume / 100, 0.0))
                self.text = self.font.render(f"volume:{Config.current_volume}", True, (255, 0, 0))
