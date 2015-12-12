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

    @property
    def image(self):
        self.rect = pygame.Rect(0, 480 - 20, 640, 20)
        image = pygame.Surface(self.rect.size)
        image.fill((127, 127, 127))
        return image


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
    global HUD
    HUD = pygame.sprite.LayeredUpdates()
    DisplayBar(HUD, forest.player)
    HealthBar(HUD, forest.player)
    AcornIndicator(HUD, forest.player)


def update():
    HUD.draw(pygame.display.get_surface())
    update.update()


update.update = pygame.display.update
pygame.display.update = update
