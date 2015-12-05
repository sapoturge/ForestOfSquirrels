import pygame


class Tree(pygame.sprite.Sprite):
    def __init__(self, forest, filename, x, y, width, depth, height):
        pygame.sprite.Sprite.__init__(self, forest)
        self.x = x
        self.y = y
        self.width = width
        self.depth = depth
        self.maxheight = height
        self.image = pygame.image.load("forestofsquirrels/graphics/{}".format(filename)).convert_alpha()
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        self.colliderect = self.rect.copy()
        self.colliderect.height = depth
        self.colliderect.width = width

    def update(self):
        self.rect.x = self.x - self.width / 2
        self.rect.y = self.y - self.height + self.depth
        self.colliderect.midbottom = self.rect.midbottom

    @classmethod
    def create_tree(cls, forest, x, y, name):
        with open("forestofsquirrels/areas/{}.tree".format(name)) as treefile:
            lines = [l.strip() for l in treefile.readlines()]
            filename = lines[0]
            trunk_width, trunk_depth, trunk_height = lines[1].split(",")
            return cls(forest, filename, x, y, int(trunk_width), int(trunk_depth), int(trunk_height))
