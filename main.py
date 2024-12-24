import pygame
import sys

from config import *
from screens.SceneHub import SceneHub

sys.setrecursionlimit(1000)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((X_SCREEN, Y_SCREEN))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()
clock.tick(FPS)

pygame.display.init()

fon = pygame.mixer.Sound('music/fon.mp3')

fon.set_volume(0.05)

fon.play(3)

scene_hub = SceneHub(screen)
scene_hub.current_scene = "MainMenuScreen"

# main
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        scene_hub.current_scene.event_handler(event)
        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #     sprite_hub.player.shoot(event.pos)

    scene_hub.current_scene.draw()
    scene_hub.current_scene.update()

    pygame.display.flip()

pygame.quit()
