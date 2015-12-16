import pygame
from .uielement import UIElement
from forestofsquirrels.core import items


class AcornIndicator(UIElement):
    def update(self):
        if isinstance(self.squirrel.inventory[0], items.Acorn):
            self.image = pygame.image.load(
                "forestofsquirrels/graphics/" + self.squirrel.inventory[0].image).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.bottom = 480
        else:
            self.image = pygame.Surface((0, 0))
