import pygame
import time
from DataBase import add_time
from Sprites.gameEntities.Gun import Backshoot, Pistol, carabin
from Sprites.viewEntities.Button import Button
from config import X_SCREEN, Y_SCREEN
from assets.assets import PLAYER_LEFT_IMG, PLAYER_RIGHT_IMG, BACKGROUND_GRAY, GREEN, BUTTON_GRAY
from skills.Freeze import Freeze


class Player(pygame.sprite.Sprite):
    def __init__(self, hub):
        pygame.sprite.Sprite.__init__(self)
        self.hub = hub

        # Загрузка изображений игрока
        self.image_right = pygame.image.load(PLAYER_RIGHT_IMG).convert()
        self.image_left = pygame.image.load(PLAYER_LEFT_IMG).convert()
        self.image = self.image_right

        # Характеристики игрока
        self.hp = 5  # Здоровье
        self.xp = 0  # Опыт
        self.level = 0  # Уровень
        self.speed_x = 0  # Скорость по оси X
        self.speed_y = 0  # Скорость по оси Y
        self.damage = 25  # Урон

        self.rect = self.image.get_rect()  # Получаем прямоугольник изображения
        self.rect.center = (X_SCREEN / 2, Y_SCREEN / 2)  # Размещаем в центре экрана

        # Выбираем начальное оружие
        # self.current_gun = Pistol(50, self.hub) #Пистолет
        self.current_gun = Backshoot(50, 5, self.hub) #Драбаш
        # self.current_gun = carabin(40, self.hub) #Карабин

        self.last_damage_time = time.time()  # Время последнего получения урона
        self.damage_cooldown = 0.25  # Кулдаун получения урона
        self.skill = Freeze() # Навык заморозки

    def take_damage(self, damage):
        """
        Уменьшает здоровье игрока, если прошло достаточно времени с последнего урона.
        """
        current_time = time.time()
        if current_time - self.last_damage_time > self.damage_cooldown: # Проверка кулдауна
            self.hp -= damage # Уменьшаем здоровье
            self.last_damage_time = current_time # Обновляем время последнего получения урона

    def give_xp(self):
        """
        Увеличивает уровень игрока, если набрано достаточно опыта.
        """
        print(f"Player XP: {self.xp}") # Выводим в консоль текущий опыт
        print(f"Player LEVEL: {self.level}") # Выводим в консоль текущий уровень
        if (self.xp >= 10): # Проверка условия повышения уровня
            self.level += 1 # Увеличиваем уровень
            self.xp = 0 # Обнуляем опыт

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
        """
        Обновляет положение игрока, обрабатывает столкновения со стенами и границами экрана.
        """
        tmp_x = self.rect.x
        tmp_y = self.rect.y
        collide = True # Изначально считаем, что столкновений нет

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if pygame.sprite.spritecollide(self, self.hub.walls, False): # Проверка столкновения со стенами
            self.rect.x = tmp_x
            self.rect.y = tmp_y
            collide = False

        # Ограничения выхода за границы экрана
        if self.rect.right > X_SCREEN:
            self.rect.right = X_SCREEN
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > Y_SCREEN:
            self.rect.bottom = Y_SCREEN
        if self.rect.top < 0:
            self.rect.top = 0
        # Сбрасываем скорость
        self.speed_x = 0
        self.speed_y = 0
        return collide # Возвращаем флаг столкновения

    def shoot(self, m_pos):
        """
        Стреляет из текущего оружия.
        """
        self.current_gun.shoot(m_pos, self.rect.centerx, self.rect.centery, self.damage)

    def draw(self, screen):
        """
        Отображает игрока на экране.
        """
        screen.blit(self.image, self.rect)  # Рисуем игрока на экране