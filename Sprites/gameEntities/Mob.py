import pygame
import random

from Sprites import EntitiesImages
from assets.assets import BLACK, WHITE, BOSS_COLOR
from config import Config


class Mob(pygame.sprite.Sprite):
    def __init__(self, hub):
        pygame.sprite.Sprite.__init__(self)
        self.hub = hub

        self.freeze = False

        if random.randint(0, 1) == 1:
            self.image = EntitiesImages.Images.red_mob
            self.type = "red"
        else:
            self.image = EntitiesImages.Images.blue_mob
            self.type = "blue"
        self.rect = self.image.get_rect()

        # ИЗМЕНЕНИЕ 1: Генерация начальной позиции так, чтобы моб не появлялся внутри стены
        self.rect.x = random.randrange(Config.Y_SCREEN - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

        # Дополнительная проверка и коррекция позиции, чтобы не появлялся в стене
        while pygame.sprite.spritecollideany(self, self.hub.walls):
            self.rect.x = random.randrange(Config.Y_SCREEN - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

        self.speed = random.randrange(1, 2)
        self.damage = 1
        self.hp = 102

        # Добавим переменные для отслеживания движения
        self.move_direction = (0, 0)  # Начальное направление (вправо)
        self.move_timer = 0  # Таймер для смены направления
        self.target_x = self.hub.player.rect.centerx  # Цель - игрок
        self.target_y = self.hub.player.rect.centery

        self.stuck = False  # Флаг, что моб столкнулся с препятствием
        self.stuck_timer = 0
        self.stuck_direction = (0, 0)  # Направление для скольжения

    def clear_effects(self):
        self.freeze = False

    def take_damage(self, damage):
        self.hp -= damage
        print(self.hp)
        if self.hp <= 0:
            self.kill()
            self.hub.player.xp += 1
            self.hub.player.give_xp()

    def draw_hp(self, screen):
        BAR_LENGTH_1 = 25
        BAR_HEIGHT_1 = 3
        fill_1 = (self.hp / 100) * BAR_LENGTH_1
        # Изменяем координаты прямоугольника для шкалы HP
        outline_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, BAR_LENGTH_1,
                                     BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, fill_1, BAR_HEIGHT_1)
        pygame.draw.rect(screen, WHITE, outline_rect_1, 2)
        pygame.draw.rect(screen, BLACK, fill_rect_1)

    def update(self):
        if self.freeze:
            return

        self.move_timer += 1
        self.target_x = self.hub.player.rect.centerx  # Обновляем цель
        self.target_y = self.hub.player.rect.centery

        if self.stuck:
            self._handle_stuck_movement()
            return

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

        # Сохраняем предыдущую позицию
        prev_x = self.rect.x
        prev_y = self.rect.y

        # Движение с учетом стенок
        self.rect.x += self.move_direction[0] * self.speed
        self.rect.y += self.move_direction[1] * self.speed

        # Проверка столкновения со стенами
        wall_collisions = pygame.sprite.spritecollide(self, self.hub.walls, False)
        if wall_collisions:
            self.rect.x = prev_x
            self.rect.y = prev_y
            # Переходим в режим "поиска выхода"
            self.stuck = True
            self.stuck_timer = 0
            self.stuck_direction = self._calculate_slide_direction(wall_collisions)

        # Проверка столкновения с игроком
        if pygame.sprite.collide_mask(self, self.hub.player):
            self.hub.player.take_damage(self.damage)

        # Удаление моба, если он выходит за границы экрана
        if self.rect.top > 900 or self.rect.left < 0 or self.rect.right > 1700:
            self.kill()

    def _handle_stuck_movement(self):
        """Обрабатывает движение, когда моб застрял."""
        self.stuck_timer += 1

        # Движение в направлении "скольжения"
        prev_x = self.rect.x
        prev_y = self.rect.y
        self.rect.x += self.stuck_direction[0] * self.speed
        self.rect.y += self.stuck_direction[1] * self.speed

        # Проверка, не освободился ли моб
        wall_collisions = pygame.sprite.spritecollide(self, self.hub.walls, False)
        if not wall_collisions:
            self.stuck = False  # Моб больше не застрял
            return

        # Если все еще застрял, возвращаем на прошлую позицию
        self.rect.x = prev_x
        self.rect.y = prev_y

        # Меняем направление скольжения
        if self.stuck_timer >= 20:
            self.stuck_timer = 0
            self.stuck_direction = (-self.stuck_direction[0], -self.stuck_direction[1])

    def _calculate_slide_direction(self, wall_collisions):
        """Вычисляет вектор скольжения вдоль стены."""
        collision = random.choice(wall_collisions)

        # Определяем направление "скольжения"
        dx = collision.rect.centerx - self.rect.centerx
        dy = collision.rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            # Двигались больше по горизонтали, значит скользим по вертикали
            return (0, 1 if dy < 0 else -1)
        else:
            # Двигались больше по вертикали, значит скользим по горизонтали
            return (1 if dx < 0 else -1, 0)


class Boss(pygame.sprite.Sprite):
    def __init__(self, hub):
        pygame.sprite.Sprite.__init__(self)
        self.hub = hub

        self.image = pygame.Surface((60, 80))  # Увеличенный размер
        self.image.fill(BOSS_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = Config.Y_SCREEN // 2 - self.rect.width // 2  # По центру по горизонтали
        self.rect.y = -100  # Сверху экрана
        self.speed = 1  # Медленнее, чем обычные враги
        self.damage = 2  # Наносит больше урона

        self.stuck = False  # Флаг, что моб столкнулся с препятствием
        self.stuck_timer = 0
        self.stuck_direction = (0, 0)  # Направление для скольжения

        self.move_direction = (0, 0)  # Начальное направление (вправо)
        self.move_timer = 0  # Таймер для смены направления
        self.target_x = self.hub.player.rect.centerx  # Цель - игрок
        self.target_y = self.hub.player.rect.centery

        self.hp = 500  # 500 очков здоровья

        # ИЗМЕНЕНИЕ 2: Генерация начальной позиции так, чтобы моб не появлялся внутри стены
        # Дополнительная проверка и коррекция позиции, чтобы не появлялся в стене
        while pygame.sprite.spritecollideany(self, self.hub.walls):
            self.rect.x = random.randrange(Config.Y_SCREEN - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

        # Добавим переменную для "плавного" движения
        self.target_x = self.rect.x
        self.target_y = self.rect.y

        # Коэффициент замедления
        self.slowdown_factor = 120  # Чем больше значение, тем медленнее движение

    def take_damage(self, damage):
        self.hp -= damage
        print(self.hp)
        if self.hp <= 0:
            self.kill()
            self.hub.player.xp += 1
            self.hub.player.give_xp()

    def draw_hp(self, screen):
        BAR_LENGTH_1 = 25
        BAR_HEIGHT_1 = 3
        fill_1 = (self.hp / 500) * BAR_LENGTH_1  # Исправлено на 500 HP
        # Изменяем координаты прямоугольника для шкалы HP
        outline_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, BAR_LENGTH_1,
                                     BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.centerx - BAR_LENGTH_1 / 2, self.rect.top - 10, fill_1, BAR_HEIGHT_1)
        pygame.draw.rect(screen, WHITE, outline_rect_1, 2)
        pygame.draw.rect(screen, BLACK, fill_rect_1)

    def update(self):
        self.move_timer += 1
        self.target_x = self.hub.player.rect.centerx  # Обновляем цель
        self.target_y = self.hub.player.rect.centery

        if self.stuck:
            self._handle_stuck_movement()
            return

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

        # Сохраняем предыдущую позицию
        prev_x = self.rect.x
        prev_y = self.rect.y

        # Движение с учетом стенок
        self.rect.x += self.move_direction[0] * self.speed
        self.rect.y += self.move_direction[1] * self.speed

        # Проверка столкновения со стенами
        wall_collisions = pygame.sprite.spritecollide(self, self.hub.walls, False)
        if wall_collisions:
            # Уничтожаем стену при столкновении
            for wall in wall_collisions:
                wall.kill()  # Уничтожаем стену
            self.rect.x = prev_x
            self.rect.y = prev_y
            # Переходим в режим "поиска выхода"
            self.stuck = True
            self.stuck_timer = 0
            self.stuck_direction = self._calculate_slide_direction(wall_collisions)

        # Проверка столкновения с пулями
        bullet_collisions = pygame.sprite.spritecollide(self, self.hub.bullets, True)
        for bullet in bullet_collisions:
            self.take_damage(bullet.damage)

        # Проверка столкновения с игроком
        if pygame.sprite.collide_mask(self, self.hub.player):
            self.hub.player.take_damage(self.damage)

        # Удаление босса, если он выходит за границы экрана
        if self.rect.top > 900 or self.rect.left < 0 or self.rect.right > 1700:
            self.kill()

    def _handle_stuck_movement(self):
        """Обрабатывает движение, когда моб застрял."""
        self.stuck_timer += 1

        # Движение в направлении "скольжения"
        prev_x = self.rect.x
        prev_y = self.rect.y
        self.rect.x += self.stuck_direction[0] * self.speed
        self.rect.y += self.stuck_direction[1] * self.speed

        # Проверка, не освободился ли моб
        wall_collisions = pygame.sprite.spritecollide(self, self.hub.walls, False)
        if not wall_collisions:
            self.stuck = False  # Моб больше не застрял
            return

        # Если все еще застрял, возвращаем на прошлую позицию
        self.rect.x = prev_x
        self.rect.y = prev_y

        # Меняем направление скольжения
        if self.stuck_timer >= 20:
            self.stuck_timer = 0
            self.stuck_direction = (-self.stuck_direction[0], -self.stuck_direction[1])

    def _calculate_slide_direction(self, wall_collisions):
        """Вычисляет вектор скольжения вдоль стены."""
        collision = random.choice(wall_collisions)

        # Определяем направление "скольжения"
        dx = collision.rect.centerx - self.rect.centerx
        dy = collision.rect.centery - self.rect.centery

        if abs(dx) > abs(dy):
            # Двигались больше по горизонтали, значит скользим по вертикали
            return (0, 1 if dy < 0 else -1)
        else:
            # Двигались больше по вертикали, значит скользим по горизонтали
            return (1 if dx < 0 else -1, 0)