import pygame

from Sprites.gameEntities.Player import Player


class SpriteHub:

    def __init__(self):
        self.all_sprites = pygame.sprite.Group()

        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()

        self.player = Player(self)

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)

    def add_wall(self, sprite):
        self.walls.add(sprite)
        self.all_sprites.add(sprite)

    def add_bullet(self, sprite):
        self.bullets.add(sprite)
        self.all_sprites.add(sprite)

    def add_mob(self, sprite):
        self.mobs.add(sprite)
        self.all_sprites.add(sprite)

    def add_boss(self, sprite):
        self.boss.add(sprite)
        self.all_sprites.add(sprite)