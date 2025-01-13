import pygame

from Sprites.viewEntities.Button import Button
from config import X_SCREEN, Y_SCREEN
from assets.assets import GREEN, BUTTON_GRAY, BACKGROUND_GRAY
from DataBase import get_total_time


class SettingsScreen:

    def __init__(self, screen, scene_hub):
        # Создание кнопок
        self.menu_button = Button(X_SCREEN // 2 - 150, Y_SCREEN // 2 - 100, 300, 50, "Go menu", BUTTON_GRAY, GREEN)
        self.screen = screen
        self.scene_hub = scene_hub
        self.total_time_text = None
        self.font = pygame.font.Font(None, 36)  # шрифт для текста

    def update(self):
        self.menu_button.update()
        total_time_seconds = get_total_time()
        hours = total_time_seconds // 3600
        minutes = (total_time_seconds % 3600) // 60
        seconds = total_time_seconds % 60
        self.total_time_text = self.font.render(f"Total Time: {hours}:{minutes:02}:{seconds:02}", True, (0, 0, 0))

    def draw(self):
        self.screen.fill(BACKGROUND_GRAY)
        self.menu_button.draw(self.screen)
        if self.total_time_text:
            text_rect = self.total_time_text.get_rect(center=(X_SCREEN // 2, Y_SCREEN // 2))
            self.screen.blit(self.total_time_text, text_rect)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.is_clicked():
                self.scene_hub.current_scene = "MainMenuScreen"