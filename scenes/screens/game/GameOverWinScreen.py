import pygame

from Sprites.viewEntities.Button import Button
from assets.assets import GREEN, BACKGROUND_GRAY, BUTTON_GRAY
from config import X_SCREEN, Y_SCREEN



class GameOverWinScreen:

    def __init__(self, screen, scene_hub):
        self.screen = screen
        self.scene_hub = scene_hub

        font = pygame.font.Font(None, 72)
        self.text = font.render("Игра окончена! Ты победил", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(center=self.screen.get_rect().center)

        self.again_button = Button(X_SCREEN // 2 - 100, Y_SCREEN // 2 + 50, 200, 50, "Сначала", BUTTON_GRAY, GREEN)
        self.main_menu_button = Button(X_SCREEN // 2 - 100, Y_SCREEN // 2 + 50 + 75, 200, 50, "Меню", BUTTON_GRAY, GREEN)

    def update(self):
        self.again_button.update()
        self.main_menu_button.update()

    def draw(self):
        self.screen.fill(BACKGROUND_GRAY)
        self.again_button.draw(self.screen)
        self.main_menu_button.draw(self.screen)
        self.screen.blit(self.text, self.text_rect)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.main_menu_button.is_clicked():
                self.scene_hub.current_scene = "MainMenuScreen"
            if self.again_button.is_clicked():
                self.scene_hub.current_scene = "GameScreen"
