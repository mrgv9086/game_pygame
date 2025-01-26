import pygame
import time

from Sprites.SpriteHub import SpriteHub
from Sprites.viewEntities.Button import Button
from scenes.screens.game.Updater import Updater
from Sprites.gameEntities.Wall import generate_walls  # Импортируем функцию генерации стен
from assets.assets import BUTTON_GRAY, GREEN, BACKGROUND_GRAY
from config import Config
from DataBase import add_time  # Импортируем функцию добавления времени

class GameScreen:
    def __init__(self, screen, scene_hub):
        self.settings_button = Button(Config.X_SCREEN // 2 - 540, Config.Y_SCREEN // 2 - 370, 50, 50, "☻", BUTTON_GRAY, GREEN)
        self.sprite_hub = SpriteHub()

        walls = generate_walls()  # функция генерации стен
        for wall in walls:  # добавление сгенерированных стен в sprite_hub
            self.sprite_hub.add_wall(wall)

        self.updater = Updater(self.sprite_hub, screen)
        self.screen = screen
        self.scene_hub = scene_hub
        self.modal_window = pygame.Surface((300, 200))
        self.modal_rect = self.modal_window.get_rect(center=(500, 300))

        self.start_time = None  # Время начала игры
        self.last_time = None  # время для сохранения в бд

    def update(self):
        update_result = self.updater.update()
        if update_result == "Loose":
            self.save_game_time()
            self.scene_hub.current_scene = "GameOverScreen"
        if update_result == "Win":
            self.save_game_time()
            self.scene_hub.current_scene = "GameOverWinScreen"
        if update_result == "level":
            self.show_player_update_modal()
        self.settings_button.update()

    def draw(self):
        self.updater.draw()
        self.settings_button.draw(self.screen)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.sprite_hub.player.shoot(event.pos)
        if self.settings_button.is_clicked():
            self.show_model()
        if not self.start_time:
            self.start_time = time.time()  # Запускаем отсчет времени

    def show_model(self):
        go_menu_button = Button(430, 270, 150, 50, "Go menu", BUTTON_GRAY, GREEN)

        # Основной цикл модального окна
        modal_active = True
        while modal_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    modal_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Закрыть модальное окно по ESC
                        modal_active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_menu_button.is_clicked():
                        self.scene_hub.current_scene = "MainMenuScreen"
                        modal_active = False

            # Отображение модального окна
            self.modal_window.fill(BACKGROUND_GRAY)  # Заполнение серым
            self.screen.blit(self.modal_window, self.modal_rect)  # Отображение модального окна
            go_menu_button.draw(self.screen)
            go_menu_button.update()
            pygame.display.flip()

    def save_game_time(self):
        if self.start_time:
            end_time = time.time()
            time_played = int(end_time - self.start_time)  #  время в секундах
            add_time(time_played)
            self.start_time = None

    # окно выбора

    def show_player_update_modal(self):
        attak_up_button = Button(350, 270, 150, 50, "attak", BUTTON_GRAY, GREEN)
        hp_up_button = Button(500, 270, 150, 50, "hp", BUTTON_GRAY, GREEN)


        # Основной цикл модального окна
        modal_active = True
        while modal_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    modal_active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if attak_up_button.is_clicked():
                        self.sprite_hub.player.damage *= 1.05
                        print("up_attak")
                        modal_active = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hp_up_button.is_clicked():
                        self.sprite_hub.player.hp *= 1.05
                        print("up_hp")
                        modal_active = False

            # Отображение модального окна
            self.modal_window.fill(BACKGROUND_GRAY)  # Заполнение серым
            self.screen.blit(self.modal_window, self.modal_rect)  # Отображение модального окна
            attak_up_button.draw(self.screen)
            attak_up_button.update()
            hp_up_button.draw(self.screen)
            hp_up_button.update()
            pygame.display.flip()