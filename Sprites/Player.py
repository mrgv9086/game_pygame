import pygame  # Импортируем Pygame
import time  # Импортируем модуль времени

from Sprites.Bullet import Bullet  # Импортируем класс пули
from Sprites.Gun import Pistol, Backshoot  # Импортируем классы оружия
from config import X_SCREEN, Y_SCREEN  # Импортируем размеры экрана
from assets import PLAYER_LEFT_IMG, PLAYER_RIGHT_IMG  # Импортируем изображения игрока

class Player(pygame.sprite.Sprite):
    def __init__(self, hub):
        pygame.sprite.Sprite.__init__(self)
        self.hub = hub

        self.image_right = pygame.image.load(PLAYER_RIGHT_IMG).convert()
        self.image_left = pygame.image.load(PLAYER_LEFT_IMG).convert()
        self.image = self.image_right
        self.hp = 5
        self.xp = 0

        self.rect = self.image.get_rect()
        self.rect.center = (X_SCREEN / 2, Y_SCREEN / 2)

        # Выбираем пистолет
        # self.current_gun = Pistol(50, self.hub)
        self.current_gun = Backshoot(50, 5, self.hub)


        self.last_damage_time = time.time()  # Время последнего урона
        self.damage_cooldown = 0.25  # Кулдаун урона

    def take_damage(self, damage):
        current_time = time.time()
        if current_time - self.last_damage_time > self.damage_cooldown:
            self.hp -= damage
            self.last_damage_time = current_time
            print(f"Player HP: {self.hp}")

            if self.hp <= 0:
                print("Player Died!")

    def give_xp (self):

        print(f"Player XP: {self.xp}")


    def update(self):
        self.speed_x = 0
        self.speed_y = 0

        tmp_x = self.rect.x
        tmp_y = self.rect.y
        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_LEFT]:
            self.speed_x = -4
            self.image = self.image_left

        if key_state[pygame.K_RIGHT]:
            self.speed_x = 4
            self.image = self.image_right

        if key_state[pygame.K_UP]:
            self.speed_y = -4

        if key_state[pygame.K_DOWN]:
            self.speed_y = 4

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if pygame.sprite.spritecollide(self, self.hub.walls, False):
            self.rect.x = tmp_x
            self.rect.y = tmp_y

        if self.rect.right > X_SCREEN:
            self.rect.right = X_SCREEN
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > Y_SCREEN:
            self.rect.bottom = Y_SCREEN
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self, m_pos):
        self.current_gun.shoot(m_pos, self.rect.centerx, self.rect.centery)