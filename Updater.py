import random

import pygame
from datetime import datetime, timedelta

from SpriteHub import SpriteHub
from Sprites.Mob import Mob
from assets import BACKGROUND, BLACK
from config import X_SCREEN, Y_SCREEN


class Updater:
    all_sprites = pygame.sprite.Group()

    def __init__(self, sprites_hub: SpriteHub, screen):
        self.hub = sprites_hub
        self.screen = screen
        self.last_mob_create_time = datetime.now()
        self.start_game_time = datetime.now()
        self.game_over_flag = False

    def update(self):
        now = datetime.now()
        if not self.game_over_flag:
            self.hub.all_sprites.update()
            self.hub.player.update()

            if now - self.start_game_time >= timedelta(seconds=150):
                return "Win"
            # Проверяем на hp
            if self.hub.player.hp <= 0:
                return "Loose"
            if now - self.last_mob_create_time >= timedelta(seconds=3):
                for i in range(random.randint(10, 20)):
                    m = Mob(self.hub)
                    self.hub.add_mob(m)
                self.last_mob_create_time = datetime.now()


    def hp_player(self):
        self.font = pygame.font.Font(None, 36)
        hp_text = self.font.render(f"HP: {self.hub.player.hp}", True, (255, 0, 0))
        self.screen.blit(hp_text, (1000, 100))

    def xp_player(self):
        self.font = pygame.font.Font(None, 36)
        xp_text = self.font.render(f"XP: {self.hub.player.xp}", True, (66, 170, 255))
        self.screen.blit(xp_text, (1000, 150))

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.hub.all_sprites.draw(self.screen)
        for mob in self.hub.mobs:
            mob.draw_hp(self.screen)
        self.screen.blit(self.hub.player.image, self.hub.player.rect)
        self.hp_player()  # Вызываем функцию для отображения HP
        self.xp_player()
