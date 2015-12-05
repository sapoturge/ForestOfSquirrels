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
        self.holes = []

    def update(self):
        self.rect.x = self.x - self.width / 2
        self.rect.y = self.y - self.height + self.depth
        self.colliderect.midbottom = self.rect.midbottom

    @classmethod
    def create_tree(cls, forest, x, y, name):
        with open("forestofsquirrels/world/trees/{}.tree".format(name)) as treefile:
            lines = [l.strip() for l in treefile.readlines()]
            filename = lines[0]
            trunk_width, trunk_depth, trunk_height = lines[1].split(",")
            tree = cls(forest, filename, x, y, int(trunk_width), int(trunk_depth), int(trunk_height))
            mode = None
            for line in lines[2:]:
                if line == "HOLES:":
                    mode = "hole"
                elif line == "SQUIRRELS:":
                    mode = "squirrel"
                elif mode == "squirrel":
                    squirrel, side, z = line.split(",")
                    import forestofsquirrels.squirrels
                    Squirrel = getattr(forestofsquirrels.squirrels, squirrel)
                    if side == "right":
                        sx = x + int(trunk_width) / 2
                    else:
                        sx = x - int(trunk_width) / 2
                    s = Squirrel(forest, sx, y)
                    s.z = z
                    s.climbing = [tree, side]
                elif mode == "hole":
                    side, bottom, top, area = line.split(",")
                    tree.holes.append((side, int(bottom), int(top), area))
        return tree
