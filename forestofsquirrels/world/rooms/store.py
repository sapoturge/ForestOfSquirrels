import pygame
import sys
from forestofsquirrels import ui
from forestofsquirrels.core import items


def main(squirrel, window, clock):
    font = pygame.font.Font("freesansbold.ttf", 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        window.fill((0, 0, 255))
        for i, item in enumerate(items.Item.items):
            window.blit(font.render(item.name, True, (0, 0, 0), (0, 0, 255)), (0, i * 20))
        clock.tick(30)
        ui.update()
