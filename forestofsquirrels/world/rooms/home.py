import pygame
import sys
from forestofsquirrels import ui


def main(squirrel, window, clock):
    window.blit(pygame.image.load("forestofsquirrels/graphics/homebackground.png"), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_s and squirrel.inventory[0] == "acorn":
                    main.acorns += 1
                    squirrel.inventory[0] = None
                elif event.key == pygame.K_a:
                    squirrel.store_left()
                elif event.key == pygame.K_d:
                    squirrel.store_right()
        ui.update()
        clock.tick(30)


main.acorns = 0
