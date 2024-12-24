from datetime import datetime, timedelta

import pygame

import random
from assets import MOBCOLOR, BLACK, WHITE, BOSS_COLOR, BLUE_MOBCOLOR
from config import Y_SCREEN


class Mob(pygame.sprite.Sprite):
    def __init__(self, hub, color=MOBCOLOR, alt_color=BLUE_MOBCOLOR):
        pygame.sprite.Sprite.__init__(self)
        self.hub = hub

        self.freeze = None
        self.freeze_time = datetime.now()
        self.reload_magic_time = datetime.now()

        self.image = pygame.Surface((30, 40))
        if random.randint(0, 1) == 1:
            self.image.fill(color)
            self.type = "red"
        else:
            self.image.fill(alt_color)
            self.type = "blue"
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(Y_SCREEN - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 2)
        self.damage = 1
        self.hp = 100

        # Добавим переменные для отслеживания движения
        self.move_direction = (0, 0)  # Начальное направление (вправо)
        self.move_timer = 0  # Таймер для смены направления
        self.target_x = self.hub.player.rect.centerx  # Цель - игрок
        self.target_y = self.hub.player.rect.centery

    def take_damage(self, damage):
        self.hp -= damage
        print(self.hp)
        if self.hp <= 0:
            self.kill()


    def draw_hp(self, screen):
        BAR_LENGTH_1 = 25
        BAR_HEIGHT_1 = 3
        fill_1 = (self.hp / 100) * BAR_LENGTH_1
        # Изменяем координаты прямоугольника для шкалы HP
        outline_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, BAR_LENGTH_1, BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, fill_1, BAR_HEIGHT_1)
        pygame.draw.rect(screen, WHITE, outline_rect_1, 2)
        pygame.draw.rect(screen, BLACK, fill_rect_1)

    def update(self):
        key_state = pygame.key.get_pressed()
        if datetime.now() - self.reload_magic_time >= timedelta(seconds=2):
            if key_state[pygame.K_q]:
                self.freeze_time = datetime.now()
                self.freeze = "red"
                self.reload_magic_time = datetime.now()
            if key_state[pygame.K_e]:
                self.freeze_time = datetime.now()
                self.freeze = "blue"
                self.reload_magic_time = datetime.now()
        if (self.type == self.freeze) and (datetime.now() - self.freeze_time <= timedelta(seconds=3)):
            return
        self.move_timer += 1
        self.target_x = self.hub.player.rect.centerx  # Обновляем цель
        self.target_y = self.hub.player.rect.centery

        # Проверяем, нужно ли изменить направление
        if self.move_timer >= 60:
            self.move_timer = 0
            # Вычисляем направление к игроку
            dx = self.target_x - self.rect.centerx
            dy = self.target_y - self.rect.centery

            # Нормализация вектора (для равномерной скорости)
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length != 0:
                dx /= length
                dy /= length

            self.move_direction = (dx, dy)

        # Движение с учетом стенок
        if self.rect.top > 900:
            self.move_direction = (self.move_direction[0], -abs(self.move_direction[1]))  # Изменяем направление, если упираемся в верхнюю стенку
        if self.rect.left < 0:
            self.move_direction = (abs(self.move_direction[0]), self.move_direction[1])  # Изменяем направление, если упираемся в левую стенку
        if self.rect.right > 1700:
            self.move_direction = (-abs(self.move_direction[0]), self.move_direction[1])  # Изменяем направление, если упираемся в правую стенку

        self.rect.x += self.move_direction[0] * self.speed
        self.rect.y += self.move_direction[1] * self.speed

        # Проверка столкновения с игроком
        if pygame.sprite.collide_mask(self, self.hub.player):
            self.hub.player.take_damage(self.damage)

        # Удаление моба, если он выходит за границы экрана
        if self.rect.top > 900 or self.rect.left < 0 or self.rect.right > 1700:
            self.kill()


# class Boss(pygame.sprite.Sprite):
#     def __init__(self, hub):
#         pygame.sprite.Sprite.__init__(self)
#         self.hub = hub
#
#         self.image = pygame.Surface((60, 80))  # Увеличенный размер
#         self.image.fill(BOSS_COLOR)
#         self.rect = self.image.get_rect()
#         self.rect.x = Y_SCREEN // 2 - self.rect.width // 2  # По центру по горизонтали
#         self.rect.y = -100  # Сверху экрана
#         self.speed = 1  # Медленнее, чем обычные враги
#         self.damage = 2  # Наносит больше урона
#         self.hp = 500  # 500 очков здоровья
#
#         # Добавим переменную для "плавного" движения
#         self.target_x = self.rect.x
#         self.target_y = self.rect.y
#
#         # Коэффициент замедления
#         self.slowdown_factor = 5  # Чем больше значение, тем медленнее движение
#
#     def take_damage(self, damage):
#         self.hp -= damage
#         print(self.hp)
#         if self.hp <= 0:
#             self.kill()
#
#     def draw_hp(self, screen):
#         BAR_LENGTH_1 = 50  # Длиннее шкала HP
#         BAR_HEIGHT_1 = 3
#         fill_1 = (self.hp / 500) * BAR_LENGTH_1  # Делим на 500, так как у босса 500 HP
#         # Изменяем координаты прямоугольника для шкалы HP
#         outline_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, BAR_LENGTH_1, BAR_HEIGHT_1)
#         fill_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, fill_1, BAR_HEIGHT_1)
#         pygame.draw.rect(screen, WHITE, outline_rect_1, 2)
#         pygame.draw.rect(screen, BLACK, fill_rect_1)
#
#     def update(self):
#         # Обновляем целевую точку, к которой движется моб
#         mouse_x = self.hub.player.rect.x
#         mouse_y = self.hub.player.rect.y
#         self.target_x = mouse_x
#         self.target_y = mouse_y
#
#         # Плавно двигаем моба к целевой точке
#         dx = (self.target_x - self.rect.centerx) / self.slowdown_factor
#         dy = (self.target_y - self.rect.centery) / self.slowdown_factor
#         self.rect.x += dx
#         self.rect.y += dy
#
#         if pygame.sprite.collide_mask(self, self.hub.player):
#             self.hub.player.take_damage(self.damage)
#
#         # Если моб выходит за границы экрана: kill
#         if self.rect.top > 900 or self.rect.left < 0 or self.rect.right > 1700:
#             self.kill()