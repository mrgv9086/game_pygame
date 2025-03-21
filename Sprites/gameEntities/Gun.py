from datetime import datetime, timedelta

from Sprites.gameEntities.Bullet import Bullet


class Guns:

    def __init__(self, damage, hub):
        self.damage = damage
        self.hub = hub
        self.reload_time = None
        self.shot = None
        self.bullet_count = None

    def reload(self, reload_time):
        if (self.reload_time is None) or (datetime.now() - self.reload_time >= timedelta(seconds=reload_time)):
            self.shot = self.bullet_count


class Pistol(Guns):
    def __init__(self, damage, hub):
        super().__init__(damage, hub)
        self.shot = 12
        self.bullet_count = 12

    def shoot(self, m_pos, player_x, player_y, player_damage):
        if self.shot >= 0:
            direction = (m_pos[1] - player_y), (m_pos[0] - player_x)
            bullet = Bullet(player_x, player_y, direction, self.hub, self.damage + player_damage)
            self.hub.add_bullet(bullet)
            self.shot -= 1
            if (self.shot == 0):
                self.reload_time = datetime.now()
        else:
            self.reload(2)


class Shotgun(Guns):
    def __init__(self, damage, bullets_count, hub):
        super().__init__(damage, hub)
        self.bullets_count = bullets_count
        self.shot = 6
        self.bullet_count = 6

    def shoot(self, m_pos, player_x, player_y, player_damage):
        if self.shot >= 0:
            for i in range(-self.bullets_count // 2, self.bullets_count // 2):
                direction = (m_pos[1] - player_y) + (20 * i), (m_pos[0] - player_x) + (20 * i)
                bullet = Bullet(player_x, player_y, direction, self.hub, self.damage + player_damage)
                self.hub.add_bullet(bullet)
            self.shot -= 1
            if (self.shot == 0):
                self.reload_time = datetime.now()
        else:
            self.reload(3)


class carabin(Guns):
    def __init__(self, damage, hub):
        super().__init__(damage, hub)
        self.shot = 30
        self.bullet_count = 30

    def shoot(self, m_pos, player_x, player_y, player_damage):
        if self.shot >= 0:
            direction = (m_pos[1] - player_y), (m_pos[0] - player_x)
            bullet = Bullet(player_x, player_y, direction, self.hub, self.damage + player_damage)
            self.hub.add_bullet(bullet)
            self.shot -= 1
            if (self.shot == 0):
                self.reload_time = datetime.now()

        else:
            self.reload(2)
