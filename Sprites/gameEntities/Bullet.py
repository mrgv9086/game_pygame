import pygame
import math

from Sprites import EntitiesImages
from Sprites.gameEntities.Mob import Mob


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, hub, damage):
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.hub = hub
        self.image = EntitiesImages.Images.bullet.convert_alpha()
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

        self.angle1 = math.cos(self.angle)
        self.angle2 = math.sin(self.angle)
    def update(self):
        self.pos_x += self.speed * self.angle1
        self.pos_y += self.speed * self.angle2

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
