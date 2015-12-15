import pygame
import sys
from forestofsquirrels import ui


def main(squirrel, window, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        window.fill((255, 255, 255))
        clock.tick(30)
        ui.update()
