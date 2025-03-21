import pygame

from assets.assets import TILE_SIZE, BUTTON_GRAY, RED_MOB_COLOR, BLUE_MOB_COLOR, BULLETCOLOR


class Images:

    wall = pygame.Surface((TILE_SIZE, TILE_SIZE))  # Размер стены равен размеру тайла
    wall.fill(BUTTON_GRAY)

    red_mob = pygame.Surface((30, 40))
    red_mob.fill(RED_MOB_COLOR)
    blue_mob = pygame.Surface((30, 40))
    blue_mob.fill(BLUE_MOB_COLOR)

    bullet = pygame.Surface((25, 10))
    bullet.fill(BULLETCOLOR)
