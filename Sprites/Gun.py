import pygame
import random

from Sprites.Bullet import Bullet
from assets import GUNCOLOR



class Guns():

    def __init__(self, damage, hub):
        self.damage = damage
        self.hub = hub


    # def shoot(self, m_pos):
    #     direction = (m_pos[0] - g.rect.x), (m_pos[1] - g.rect.y)
    #     bullet = Bullet(self.rect.centerx, self.rect.top, direction)
    #     all_sprites.add(bullet)
    #      bullets.add(bullet)


class Pistol(Guns):
    def __init__(self, damage, hub):
        super().__init__(damage, hub)

    def shoot(self, m_pos, player_x, player_y):
        direction = (m_pos[1] - player_y), (m_pos[0] - player_x)
        bullet = Bullet(player_x, player_y, direction, self.hub, self.damage)
        self.hub.add_bullet(bullet)

class Backshoot(Guns):
    def __init__(self, damage, bullets_count, hub):
        super().__init__(damage, hub)
        self.bullets_count = bullets_count

    def shoot(self, m_pos, player_x, player_y):
        for i in range(self.bullets_count):
            tmp = True
            if tmp == True:
                direction = (m_pos[1] - player_y - i * 10), (m_pos[0] - player_x - i * 10)
                tmp = False
            else:
                direction = (m_pos[1] - player_y - i * 10), (m_pos[0] - player_x - i * 10)
                tmp = True
            bullet = Bullet(player_x, player_y, direction, self.hub, self.damage)
            self.hub.add_bullet(bullet)