import pygame


class UIElement(pygame.sprite.Sprite):
    def __init__(self, group, squirrel):
        self.squirrel = squirrel
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.level = 0
        pygame.sprite.Sprite.__init__(self, group)


class DisplayBar(UIElement):
    def __init__(self, group, squirrel):
        UIElement.__init__(self, group, squirrel)
        self.level = 1
        self.rect = pygame.Rect(0, 480 - 20, 640, 20)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((127, 127, 127))
