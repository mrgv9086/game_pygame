import pygame
from assets import GUNCOLOR, BUTTON_TEXT_COLOR


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, color, hover_color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.x < mouse_pos[0] < self.rect.x + self.rect.width and self.rect.y < mouse_pos[
            1] < self.rect.y + self.rect.height and pygame.mouse.get_pressed()[0]

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if (self.rect.x < mouse_pos[0] < self.rect.x + self.rect.width
                and self.rect.y < mouse_pos[1] < self.rect.y + self.rect.height):
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.color)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

