import pygame
import random

from pygame import Rect

from Sprites import EntitiesImages
from Sprites.gameEntities.Player import Player
from assets.assets import BUTTON_GRAY, TILE_SIZE, GRID_HEIGHT, GRID_WIDTH
from config import Config


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = EntitiesImages.Images.wall
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE  # Устанавливаем x на основе тайловой сетки
        self.rect.y = y * TILE_SIZE  # Устанавливаем y на основе тайловой сетки


def generate_walls(player: Player):

    clear_place: Rect = player.rect.copy()
    clear_place.width = clear_place.width * 4
    clear_place.height = clear_place.height * 4
    clear_place.center = player.rect.center

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
                if clear_place.colliderect(wall):
                    continue
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
