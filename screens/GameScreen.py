import pygame

from SpriteHub import SpriteHub
from Sprites.Button import Button
from Updater import Updater
from Sprites.Wall import Wall
from Sprites.Mob import Mob
from assets import BUTTON_GRAY, GREEN
from config import X_SCREEN, Y_SCREEN


class GameScreen:
    def __init__(self, screen, scene_hub):
        self.settings_button = Button(X_SCREEN // 2 - 540, Y_SCREEN //2 - 370, 50, 50, "☻", BUTTON_GRAY, GREEN)

        self.sprite_hub = SpriteHub()

        for i in range(15):
            w = Wall()
            self.sprite_hub.add_wall(w)

        self.updater = Updater(self.sprite_hub, screen)
        self.screen = screen
        self.scene_hub = scene_hub
        self.modal_window = pygame.Surface((200, 150))
        self.modal_rect = self.modal_window.get_rect(center=(200, 150))


    def update(self):
        if self.updater.update() == "Loose":
            self.scene_hub.current_scene = "GameOverScreen"
        if self.updater.update() == "Win":
            self.scene_hub.current_scene = "GameOverWinScreen"
        self.settings_button.update()

    def draw(self):
        self.updater.draw()
        self.settings_button.draw(self.screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.sprite_hub.player.shoot(event.pos)
        if self.settings_button.is_clicked():
            self.show_model()

    def show_model(self):
        pygame.display.set_mode((200, 150), pygame.NOFRAME)  # Убираем рамку
        pygame.display.set_caption("Модальное окно")

        # Основной цикл модального окна
        modal_active = True
        while modal_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    modal_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Закрыть модальное окно по ESC
                        modal_active = False

            # Отображение модального окна
            self.modal_window.fill((255, 255, 255))  # Заполнение белым
            pygame.draw.rect(self.modal_window, (200, 0, 0), (20, 20, 160, 110))  # Красная рамка
            self.screen.blit(self.modal_window, self.modal_rect)  # Отображение модального окна
            pygame.display.flip()
