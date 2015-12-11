import pygame


class UIElement(pygame.sprite.Sprite):
    def __init__(self, group, squirrel):
        self.squirrel = squirrel
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.y = 0
        pygame.sprite.Sprite.__init__(self, group)


class HealthBar(UIElement):
    @property
    def image(self):
        image = pygame.Surface((self.squirrel.health * 16, 16)).convert_alpha()
        image.fill((0, 0, 0, 0))
        for y in range(self.squirrel.health):
            pygame.draw.circle(image, (255, 0, 0), (y * 16 + 8, 8), 8)
        self.rect = image.get_rect()
        self.rect.bottomright = (640, 480)
        return image


class AcornIndicator(UIElement):
    @property
    def image(self):
        if self.squirrel.acorn:
            image = pygame.image.load("forestofsquirrels/graphics/acorn.png").convert_alpha()
            self.rect = image.get_rect()
            self.rect.bottom = 480
            return image
        return pygame.Surface((0, 0))


def create_ui(forest):
    HealthBar(forest, forest.player)
    AcornIndicator(forest, forest.player)
