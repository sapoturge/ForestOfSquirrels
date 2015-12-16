import pygame
import sys
from forestofsquirrels.core import items


def main(squirrel, window, clock):
    current_category = items.categories.keys()[0]
    font = pygame.font.Font("freesansbold.ttf", 20)
    window.fill((0, 0, 255))
    mode_rects, category_rects = draw_tabs(window, font, items.categories, current_category)
    mode = "buy"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for c in category_rects:
                    if category_rects[c].collidepoint(event.pos):
                        current_category = c
                        window.fill((0, 0, 255))
                        draw_tabs(window, font, items.categories, current_category)
        for i, item in enumerate(items.categories[current_category]):
            window.blit(font.render(item.name, True, (0, 0, 0), (0, 0, 255)), (50, i * 20 + 50))
        clock.tick(30)
        pygame.display.update()


def draw_tabs(window, font, categories, current_category):
    pygame.draw.rect(window, (255, 255, 255), (0, 0, 640, 40))
    pygame.draw.rect(window, (128, 128, 255), (0, 40, 40, 440))
    y = 42
    rects = {}
    for c in categories.keys():
        color = (0, 0, 255) if c == current_category else (192, 192, 192)
        basesurf = font.render(c, True, (0, 0, 0), color)
        newsurf = pygame.Surface((basesurf.get_width() + 20, 39))
        newsurf.fill((128, 128, 255))
        pygame.draw.rect(newsurf, color, (0, 10, newsurf.get_width(), 29))
        pygame.draw.rect(newsurf, color, (10, 0, newsurf.get_width() - 20, 10))
        pygame.draw.circle(newsurf, color, (10, 10), 10)
        pygame.draw.circle(newsurf, color, (newsurf.get_width() - 10, 10), 10)
        baserect = basesurf.get_rect()
        newrect = newsurf.get_rect()
        baserect.midbottom = newrect.midbottom
        newsurf.blit(basesurf, baserect)
        rects[c] = window.blit(pygame.transform.rotate(newsurf, 90), (1, y))
        y += newsurf.get_width() + 4
    return [], rects
