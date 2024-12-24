import pygame
import random

from assets import BUTTON_GRAY
from config import Y_SCREEN, X_SCREEN


class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(BUTTON_GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, X_SCREEN - 30)
        self.rect.y = random.randint(0, Y_SCREEN - 40)

        # self.generate_pile()

    # def generate_pile(self):
    #     self.rect.x = random.randint(0, 100)
    #     self.rect.y = random.randint(0, 100)
    #
    #     for i in range(4):
    #         offset_x = random.randint(-15, 15)
    #         offset_y = random.randint(-15, 15)
    #
    #         new_stone = Wall()
    #         new_stone.rect.x = self.rect.x + offset_x
    #         new_stone.rect.y = self.rect.y + offset_y
    #
    #         if not pygame.sprite.collide_rect(self, new_stone):
    #             new_stone.rect = new_stone.rect
    #         else:
    #             new_stone.rect.x += 20
    #             new_stone.rect.y += 20