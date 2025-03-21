import random

import pygame
from datetime import datetime, timedelta

from Sprites.SpriteHub import SpriteHub
from Sprites.gameEntities.Mob import Mob, Boss
from assets.assets import BACKGROUND


class Updater:
    all_sprites = pygame.sprite.Group()

    def __init__(self, sprites_hub: SpriteHub, screen):
        self.hub = sprites_hub
        self.screen = screen
        self.last_mob_create_time = datetime.now()
        self.start_game_time = datetime.now()
        self.game_over_flag = False
        self.font = pygame.font.Font(None, 36)
        self.n = 0
        self.schetcik = 0

        self.offset_speed_x = 0
        self.offset_speed_y = 0

    def clear_mobs_effects(self):
        for mob in self.hub.mobs:
            mob.clear_effects()

    def update(self):

        if self.hub.player.level >= 5:
            self.hub.player.level = 0
            return "level"
        if not self.hub.player.skill.is_active():
            self.clear_mobs_effects()

        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.hub.player.move_up()
            self.offset_speed_y = 4
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            self.hub.player.move_down()
            self.offset_speed_y = -4
        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.hub.player.move_left()
            self.offset_speed_x = 4
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.hub.player.move_right()
            self.offset_speed_x = -4
        if key_state[pygame.K_e] or key_state[pygame.K_q]:
            mob_to_freeze = self.hub.player.skill.use(key_state)
            if mob_to_freeze is not None:
                for mob in self.hub.mobs:
                    if mob.type == mob_to_freeze:
                        mob.freeze = True

        now = datetime.now()
        if not self.game_over_flag:
            self.hub.all_sprites.update()
            if not self.hub.player.update():
                for sprite in self.hub.walls:
                    sprite.rect.x += self.offset_speed_x
                    sprite.rect.y += self.offset_speed_y
                for sprite in self.hub.mobs:
                    sprite.rect.x += self.offset_speed_x
                    sprite.rect.y += self.offset_speed_y
                for sprite in self.hub.bullets:
                    sprite.pos_x += self.offset_speed_x
                    sprite.pos_y += self.offset_speed_y
            self.offset_speed_x = 0
            self.offset_speed_y = 0

            if now - self.start_game_time >= timedelta(seconds=1000):
                return "Win"
            # Проверяем на hp
            if self.hub.player.hp <= 0:
                return "Loose"
            if len(self.hub.mobs) <= 40:
                if now - self.last_mob_create_time >= timedelta(seconds=4): #mob time
                    for i in range(random.randint(10, 20)):
                        m = Mob(self.hub)
                        if self.n == 30:
                            m.hp += 500
                        self.hub.add_mob(m)
                        self.n+=10
                    self.last_mob_create_time = datetime.now()
                    self.schetcik += 1
                    self.bosses()

    def bosses(self):
        if (self.schetcik % 3 == 0):
            B = Boss(self.hub)
            self.hub.add_boss(B)

    def hp_player(self):
        hp_text = self.font.render(f"HP: {self.hub.player.hp}", True, (255, 0, 0))
        self.screen.blit(hp_text, (1000, 100))

    def xp_player(self):
        xp_text = self.font.render(f"XP: {self.hub.player.xp}", True, (66, 170, 255))
        self.screen.blit(xp_text, (1000, 150))

    def draw(self):
        self.screen.fill(BACKGROUND)

        self.hub.all_sprites.draw(self.screen)
        for mob in self.hub.mobs:
            mob.draw_hp(self.screen)

        self.hub.player.draw(self.screen)

        self.hp_player()  # Вызываем функцию для отображения HP
        self.xp_player()
