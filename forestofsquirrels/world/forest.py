import pygame

import forestofsquirrels.squirrels
import forestofsquirrels.trees


class Area(pygame.sprite.Sprite, pygame.sprite.AbstractGroup):
    def __init__(self, forest, x, y, area_name):
        self.x = x
        self.y = y
        self.forest = forest
        self.connections = {}
        pygame.sprite.Sprite.__init__(self, forest)
        pygame.sprite.AbstractGroup.__init__(self)
        with open("forestofsquirrels/world/areas/{}.area".format(area_name)) as area:
            lines = [l.strip() for l in area.readlines()]
            width, height = lines[0].split(",")
            self.width = int(width)
            self.height = int(height)
            mode = None
            for line in lines[1:]:
                if line == "TREES:":
                    mode = "tree"
                elif line == "CONNECTIONS:":
                    mode = "connection"
                elif mode == "tree":
                    tree, x, y = line.split(",")
                    forestofsquirrels.trees.Tree.create_tree(self, int(x), int(y), tree)
                elif mode == "connection":
                    side, area = line.split(",")
                    self.connections[side] = area
        for s in self.sprites():
            s.x -= self.x
            s.y -= self.y
            if isinstance(s, forestofsquirrels.squirrels.Player):
                self.remove_internal(s)
            forest.add_internal(s)
            s.add_internal(forest)
        self.dead = False
        self.image = pygame.Surface((0, 0))
        self.forest.player = self.player
        self.player.forest = self.forest

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if not self.rect.colliderect(self.forest.screenrect.inflate(1280, 960)):
            if not self.dead:
                for s in self.sprites():
                    self.forest.remove(s)
                self.dead = True
        elif self.dead:
            for s in self.sprites():
                self.forest.add(s)
            self.dead = False

    def add_internal(self, other):
        if isinstance(other, pygame.sprite.AbstractGroup):
            pygame.sprite.Sprite.add_internal(self, other)
        else:
            pygame.sprite.AbstractGroup.add_internal(self, other)

    def remove_internal(self, other):
        if isinstance(other, pygame.sprite.AbstractGroup):
            pygame.sprite.Sprite.remove_internal(self, other)
        else:
            pygame.sprite.AbstractGroup.remove_internal(self, other)


class Forest(pygame.sprite.LayeredUpdates):
    def __init__(self, camera_x=0, camera_y=0):
        self.camera_x = camera_x
        self.camera_y = camera_y
        self.screenrect = pygame.Rect(camera_x, camera_y, 640, 480)
        pygame.sprite.LayeredUpdates.__init__(self)

    def update(self):
        for s in self.sprites():
            s.update()
        # self.camera_x = min(max(self.camera_x, 0), self.width - 640)
        # self.camera_y = min(max(self.camera_y, 0), self.height - 480)
        for s in self.sprites():
            s.rect.x -= self.camera_x
            s.rect.y -= self.camera_y
        self.screenrect = pygame.Rect(self.camera_x, self.camera_y, 640, 480)

    def draw(self, surface):
        for spr in sorted(self.sprites(), key=lambda s: s.y):
            surface.blit(spr.image, spr.rect)
