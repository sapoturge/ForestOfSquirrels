import pygame
from .uielement import UIElement


class HealthBar(UIElement):
    def update(self):
        self.image = pygame.Surface((self.squirrel.health * 18, 18)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        for y in range(self.squirrel.health):
            pygame.draw.circle(self.image, (255, 0, 0), (y * 18 + 9, 9), 8)
        self.rect = self.image.get_rect()
        self.rect.bottomright = (640, 480)
