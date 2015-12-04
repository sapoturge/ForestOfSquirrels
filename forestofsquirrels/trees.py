import pygame


class Tree(pygame.sprite.Sprite):
    def __init__(self, forest, x, y):
        pygame.sprite.Sprite.__init__(self, forest)
        self.x = x
        self.y = y
        self.image = pygame.image.load("forestofsquirrels/graphics/tree.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.colliderect = self.rect.copy()
        self.colliderect.height = self.width / 3
        self.colliderect.width = self.width / 2

    def update(self):
        self.rect.x = self.x - self.width / 2
        self.rect.y = self.y - self.height + 20
        self.colliderect.midbottom = self.rect.midbottom
