from datetime import datetime, timedelta

import pygame

from Sprites.gameEntities.Bullet import Bullet


class Guns():
    """
    Базовый класс для всех видов оружия.
    Содержит общую логику для перезарядки и стрельбы.
    """

    def __init__(self, damage, hub):
        self.damage = damage
        self.hub = hub
        self.reload_time = None  # Время последней перезарядки (None, если еще не перезаряжалось)
        self.shot = None  # Количество оставшихся патронов в магазине
        self.bullet_count = None  # Максимальное количество патронов в магазине

    def reload(self, reload_time):
        """
        Перезаряжает оружие, если прошло достаточно времени с последней перезарядки.
        """
        if (self.reload_time is None) or (datetime.now() - self.reload_time >= timedelta(seconds=reload_time)):
            self.shot = self.bullet_count  # Восстанавливаем количество патронов до максимального


class Pistol(Guns):
    """
    Класс, представляющий пистолет.
    Наследуется от класса Guns.
    """

    def __init__(self, damage, hub):
        super().__init__(damage, hub)
        self.shot = 12
        self.bullet_count = 12

    def shoot(self, m_pos, player_x, player_y, player_damage):
        """
        Производит выстрел из пистолета.
        """
        if self.shot >= 0:
            direction = (m_pos[1] - player_y), (m_pos[0] - player_x)
            bullet = Bullet(player_x, player_y, direction, self.hub,
                            self.damage + player_damage)
            self.hub.add_bullet(bullet)
            self.shot -= 1
            if (self.shot == 0):
                self.reload_time = datetime.now()
        else:
            self.reload(2)


class Backshoot(Guns):
    """
    Класс, представляющий оружие, стреляющее веером пуль.
    Наследуется от класса Guns.
    """

    def __init__(self, damage, bullets_count, hub):
        """
        Инициализирует оружие, стреляющее веером.

        Args:
            damage (int): Урон оружия.
            bullets_count (int): Количество пуль в веере.
            hub (Hub): Ссылка на игровой хаб.
        """
        super().__init__(damage, hub)
        self.bullets_count = bullets_count  # Количество пуль в веере
        self.shot = 6  # Начальное количество патронов в магазине
        self.bullet_count = 6  # Максимальное количество патронов в магазине

    def shoot(self, m_pos, player_x, player_y, player_damage):
        """
        Производит выстрел веером пуль.

        Args:
            m_pos (tuple): Позиция мыши (куда стреляем).
            player_x (int): X-координата игрока.
            player_y (int): Y-координата игрока.
            player_damage (int): Дополнительный урон игрока.
        """
        if self.shot >= 0:  # Если есть патроны
            for i in range(-self.bullets_count // 2,
                           self.bullets_count // 2):  # Цикл для создания пуль в веере
                direction = (m_pos[1] - player_y) + (20 * i), (m_pos[0] - player_x) + (20 * i)  # Направление для каждой пули
                bullet = Bullet(player_x, player_y, direction, self.hub,
                                self.damage + player_damage)  # Создаем пулю
                self.hub.add_bullet(bullet)  # Добавляем пулю в игру
            self.shot -= 1  # Уменьшаем количество патронов
            if (self.shot == 0):  # Если патроны закончились
                self.reload_time = datetime.now()  # Устанавливаем время перезарядки
        else:
            self.reload(3)  # Перезаряжаем, если патроны закончились


class carabin(Guns):
    """
    Класс, представляющий карабин.
    Наследуется от класса Guns.
    """

    def __init__(self, damage, hub):
        super().__init__(damage, hub)
        self.shot = 30  # Начальное количество патронов в магазине
        self.bullet_count = 30  # Максимальное количество патронов в магазине

    def shoot(self, m_pos, player_x, player_y, player_damage):
        """
         Производит выстрел из карабина.
        """
        if self.shot >= 0:
            direction = (m_pos[1] - player_y), (m_pos[0] - player_x)
            bullet = Bullet(player_x, player_y, direction, self.hub,
                            self.damage + player_damage)
            self.hub.add_bullet(bullet)
            self.shot -= 1
            if (self.shot == 0):
                self.reload_time = datetime.now()
        else:
            self.reload(2)