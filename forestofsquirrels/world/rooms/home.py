import sys
import pygame


def main(window, clock):
    window.blit(pygame.image.load("forestofsquirrels/graphics/homebackground.png"), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.update()
        clock.tick(30)
