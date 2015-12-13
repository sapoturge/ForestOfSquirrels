import pygame
from .uielement import UIElement


class AcornIndicator(UIElement):
    def update(self):
        if self.squirrel.inventory[0] == "acorn":
            self.image = pygame.image.load("forestofsquirrels/graphics/acorn.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.bottom = 480
        else:
            self.image = pygame.Surface((0, 0))
