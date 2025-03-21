import pygame

from config import Config
from scenes.SceneHub import SceneHub

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Config.X_SCREEN, Config.Y_SCREEN))
pygame.display.set_caption(Config.CAPTION)
clock = pygame.time.Clock()
clock.tick(Config.FPS)

pygame.display.init()

Config.fon.set_volume(0.2)

Config.fon.play(3)

scene_hub = SceneHub(screen)
scene_hub.current_scene = "MainMenuScreen"

# main
run = True
while run:
    clock.tick(Config.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        scene_hub.current_scene.event_handler(event)

    scene_hub.current_scene.draw()
    scene_hub.current_scene.update()

    pygame.display.flip()

pygame.quit()
