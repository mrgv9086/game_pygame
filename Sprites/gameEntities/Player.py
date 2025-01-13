import pygame  # Импортируем Pygame
import time  # Импортируем модуль времени

from DataBase import add_time
from Sprites.gameEntities.Gun import Backshoot, Pistol, carabin  # Импортируем классы оружия
from Sprites.viewEntities.Button import Button
from config import X_SCREEN, Y_SCREEN  # Импортируем размеры экрана
from assets.assets import PLAYER_LEFT_IMG, PLAYER_RIGHT_IMG, BACKGROUND_GRAY, GREEN, BUTTON_GRAY
from skills.Freeze import Freeze


class Player(pygame.sprite.Sprite):
    def __init__(self, hub):
        pygame.sprite.Sprite.__init__(self)
        self.hub = hub

        self.image_right = pygame.image.load(PLAYER_RIGHT_IMG).convert()
        self.image_left = pygame.image.load(PLAYER_LEFT_IMG).convert()
        self.image = self.image_right
        self.hp = 5
        self.xp = 0
        self.level = 0
        self.speed_x = 0
        self.speed_y = 0
        self.damage = 25

        self.rect = self.image.get_rect()
        self.rect.center = (X_SCREEN / 2, Y_SCREEN / 2)

        # Выбираем оружее
        # self.current_gun = Pistol(50, self.hub)
        self.current_gun = Backshoot(50, 5, self.hub)
        # self.current_gun = carabin(40, self.hub)

        self.last_damage_time = time.time()  # Время последнего урона
        self.damage_cooldown = 0.25  # Кулдаун урона
        self.skill = Freeze()

    def take_damage(self, damage):
        current_time = time.time()
        if current_time - self.last_damage_time > self.damage_cooldown:
            self.hp -= damage
            self.last_damage_time = current_time

    def give_xp(self):

        print(f"Player XP: {self.xp}")
        print(f"Player LEVEL: {self.level}")
        if (self.xp >= 10):
            self.level += 1
            self.xp = 0




    def move_left(self):
        self.speed_x = -4
        self.image = self.image_left

    def move_right(self):
        self.speed_x = 4
        self.image = self.image_right

    def move_up(self):
        self.speed_y = -4

    def move_down(self):
        self.speed_y = 4

    def update(self):
        tmp_x = self.rect.x
        tmp_y = self.rect.y
        collide = True

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if pygame.sprite.spritecollide(self, self.hub.walls, False):
            self.rect.x = tmp_x
            self.rect.y = tmp_y
            collide = False


        if self.rect.right > X_SCREEN:
            self.rect.right = X_SCREEN
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > Y_SCREEN:
            self.rect.bottom = Y_SCREEN
        if self.rect.top < 0:
            self.rect.top = 0

        self.speed_x = 0
        self.speed_y = 0
        return collide

    def shoot(self, m_pos):
        self.current_gun.shoot(m_pos, self.rect.centerx, self.rect.centery, self.damage)

    def draw(self, screen):
        screen.blit(self.image, self.rect)