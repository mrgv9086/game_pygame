import pygame
import random

from assets.assets import BUTTON_GRAY
from config import Config

TILE_SIZE = 30  # Размер одного тайла
GRID_WIDTH = Config.X_SCREEN * 4 // TILE_SIZE  # Ширина сетки в тайлах
GRID_HEIGHT = Config.Y_SCREEN * 4 // TILE_SIZE  # Высота сетки в тайлах


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))  # Размер стены равен размеру тайла
        self.image.fill(BUTTON_GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE  # Устанавливаем x на основе тайловой сетки
        self.rect.y = y * TILE_SIZE  # Устанавливаем y на основе тайловой сетки


def generate_walls():
    """Генерирует стены на основе клеточного автомата."""
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]  # Инициализация пустой сетки

    # Заполняем сетку случайными стенами для начала
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if random.random() < 0.4:  # 40% вероятность, что клетка будет стеной
                grid[y][x] = 1

    # Применяем клеточный автомат несколько раз для создания органичной структуры
    for _ in range(4):  # Несколько итераций клеточного автомата
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbor_walls = count_neighbor_walls(grid, x, y)

                if grid[y][x] == 1:
                    if neighbor_walls < 4:
                        new_grid[y][x] = 0  # Если слишком мало соседей, стена исчезает
                    else:
                        new_grid[y][x] = 1  # Если достаточно соседей, стена остается
                else:
                    if neighbor_walls > 4:
                        new_grid[y][x] = 1  # Если много соседей, то появляется стена
        grid = new_grid

    # Создаем рамку из стен
    for y in range(GRID_HEIGHT):
        grid[y][0] = 1
        grid[y][GRID_WIDTH - 1] = 1
    for x in range(GRID_WIDTH):
        grid[0][x] = 1
        grid[GRID_HEIGHT - 1][x] = 1

    # Создаем спрайты стен на основе полученной сетки
    walls = pygame.sprite.Group()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                wall = Wall(x, y)
                walls.add(wall)

    return walls


def count_neighbor_walls(grid, x, y):
    """Считает количество соседних стен."""
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 1:
                count += 1
    return count


def handle_player_collisions(player, walls):
    """Обрабатывает столкновения игрока со стенами с эффектом "скольжения"."""

    player_rect = player.rect.copy()  # Получаем копию прямоугольника игрока

    # Проверяем столкновение с каждым направлением и выполняем коррекцию
    collision_x = False
    collision_y = False

    # Горизонтальные столкновения
    player_rect.x += player.speed_x
    collisions = pygame.sprite.spritecollide(player, walls, False)
    if collisions:
        collision_x = True
        if player.speed_x > 0:
            player.rect.right = collisions[0].rect.left
        elif player.speed_x < 0:
            player.rect.left = collisions[0].rect.right

    # Вертикальные столкновения
    player_rect = player.rect.copy()  # Обновляем rect для проверки по y
    player_rect.y += player.speed_y
    collisions = pygame.sprite.spritecollide(player, walls, False)

    if collisions:
        collision_y = True
        if player.speed_y > 0:
            player.rect.bottom = collisions[0].rect.top
        elif player.speed_y < 0:
            player.rect.top = collisions[0].rect.bottom

    # Применяем эффект скольжения, если было столкновение
    if collision_x and not collision_y:
        player.speed_x = 0  # Останавливаем движение по x, но оставляем y

    if not collision_x and collision_y:
        player.speed_y = 0  # Останавливаем движение по y, но оставляем x

    if collision_x and collision_y:
        player.speed_x = 0
        player.speed_y = 0