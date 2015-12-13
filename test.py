import pygame
import sys
from forestofsquirrels.world.simplexnoise import SimplexNoise

noise = SimplexNoise(28)

window = pygame.display.set_mode((512, 512))

min_x = 0
min_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                min_y += 1
            elif event.key == pygame.K_UP:
                min_y -= 16
            elif event.key == pygame.K_RIGHT:
                min_x += 16
            elif event.key == pygame.K_LEFT:
                min_x -= 16
    for x in range(512):
        for y in range(512):
            c = int(((noise.noise2d((x + min_x) / 1024.0, (y + min_y) / 1024.0) * 4) ** 2) * 8)
            if c == 0:
                color = (0, 0, 255)
            else:
                color = (127 + c, 128 - c, 0)
            try:
                window.set_at((x, y), color)
            except TypeError:
                print color
    print "Done!"
    pygame.display.update()
