import pygame
import math

from Sprites.gameEntities.Mob import Mob
from assets.assets import BULLETCOLOR

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, hub, damage):
        # Инициализация спрайта
        pygame.sprite.Sprite.__init__(self)
        # Урон, наносимый пулей
        self.damage = damage
        # Ссылка на игровой хаб (для доступа к другим объектам игры)
        self.hub = hub
        # Создание поверхности для изображения пули (прямоугольник 25x10 пикселей)
        self.image = pygame.Surface((25, 10)).convert_alpha()
        # Заполнение поверхности цветом пули из assets
        self.image.fill(BULLETCOLOR)
        # Направление движения пули (вектор)
        self.direction = direction

        # Расчет угла поворота пули в радианах, arctan2 вернет угол правильно в 4 квадрантах
        self.angle = math.atan2(self.direction[0], self.direction[1])
        # Расчет угла в градусах, отрицательный чтобы учесть поворот pygame
        self.angle_deg = -math.degrees(self.angle)

        # Поворот изображения пули на вычисленный угол
        self.image = pygame.transform.rotate(self.image, self.angle_deg)
        # Создание прямоугольника для колизии пули
        self.rect = pygame.Rect(x, y, 25, 10)
        # Установка центра прямоугольника в координаты x и y
        self.rect.centery = y
        self.rect.centerx = x

        # Сохранение позиции пули как вещественные числа
        self.pos_x = self.rect.centerx
        self.pos_y = self.rect.centery

        # Скорость движения пули
        self.speed = 10

    def update(self):
        # Обновление позиции пули на основе скорости и угла
        self.pos_x += self.speed * math.cos(self.angle)
        self.pos_y += self.speed * math.sin(self.angle)

        # Обновление позиции прямоугольника колизии
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        # Проверка столкновений с мобами
        collide_sprites = pygame.sprite.spritecollide(self, self.hub.mobs, False)
        # Обработка столкновений с мобами
        for sprite in collide_sprites:
            if isinstance(sprite, Mob):
                # Нанесение урона мобу
                sprite.take_damage(self.damage)
                # Уничтожение пули после столкновения
                self.kill()

        # Уничтожение пули, если она выходит за границы экрана
        if self.rect.bottom < 0 or self.rect.top > 900 or self.rect.left < 0 or self.rect.right > 1700:
            self.kill()