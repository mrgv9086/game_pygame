import pygame
import math

from Sprites.Mob import Mob
from assets import BULLETCOLOR

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, hub, damage):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.hub = hub
        self.image = pygame.Surface((25, 10)).convert_alpha()
        self.image.fill(BULLETCOLOR)
        self.direction = direction

        self.angle = math.atan2(self.direction[0], self.direction[1])
        self.angle_deg = -math.degrees(self.angle)

        self.image = pygame.transform.rotate(self.image, self.angle_deg)
        self.rect = pygame.Rect(x, y, 25, 10)
        self.rect.centery = y
        self.rect.centerx = x

        self.pos_x = self.rect.centerx
        self.pos_y = self.rect.centery

        self.speed = 10

    def update(self):
        self.pos_x += self.speed * math.cos(self.angle)
        self.pos_y += self.speed * math.sin(self.angle)

        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        collide_sprites = pygame.sprite.spritecollide(self, self.hub.mobs, False)
        for sprite in collide_sprites:
            if isinstance(sprite, Mob):
                sprite.take_damage(self.damage)
                self.kill()

        # уничтожить, если пуля заходит за экран
        if self.rect.bottom < 0 or self.rect.top > 900 or self.rect.left < 0 or self.rect.right > 1700:
            self.kill()
