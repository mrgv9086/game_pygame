import pygame
# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, player_img_right, player_img_left, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image_right = player_img_right
        self.image_left = player_img_left
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, walls):
        self.speedx = 0
        self.speedy = 0
        tmp_x = self.rect.x
        tmp_y = self.rect.y
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -4
            self.image = self.image_left


        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
            self.image = self.image_right

        if keystate[pygame.K_UP]:
            self.speedy = -4


        if keystate[pygame.K_DOWN]:
            self.speedy = 4


        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = tmp_x
            self.rect.y = tmp_y



        if self.rect.right > 1700:
            self.rect.right = 1700
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > 900:
            self.rect.bottom = 900
        if self.rect.top < 0:
            self.rect.top = 0