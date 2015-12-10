import pygame

import forestofsquirrels.squirrels
import forestofsquirrels.trees


class Area(pygame.sprite.Sprite, pygame.sprite.AbstractGroup):
    def __init__(self, forest, x, y, area_name):
        self.forest = forest
        self.connections = {}
        self.realx = x
        self.realy = y
        self.forest.areas[x, y] = self
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
                    tree, tx, ty = line.split(",")
                    forestofsquirrels.trees.Tree.create_tree(self, int(tx), int(ty), tree)
                elif mode == "connection":
                    side, area = line.split(",")
                    self.connections[side] = area
        self.x = x * self.width
        self.y = y * self.height
        for s in self.sprites():
            s.x += self.x
            s.y += self.y
            if isinstance(s, forestofsquirrels.squirrels.Player):
                self.remove_internal(s)
            forest.add_internal(s)
            s.add_internal(forest)
        self.dead = False
        self.image = pygame.Surface((0, 0))
        if hasattr(self, "player"):
            self.forest.player = self.player
            self.player.forest = self.forest

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        bigrect = self.forest.screenrect.inflate(1280, 960)
        if not (self.rect.colliderect(bigrect) or bigrect.contains(self.rect)):
            if not self.dead:
                for s in self.sprites():
                    self.forest.remove(s)
                self.dead = True
                print("Dead at {}, {} ({}, {})!".format(self.x, self.y, self.realx, self.realy))
                print(bigrect)
        elif self.dead:
            for s in self.sprites():
                self.forest.add(s)
            self.dead = False
        if bigrect.contains(self.rect):
            if (self.realx, self.realy + 1) not in self.forest.areas:
                Area(self.forest, self.realx, self.realy + 1, "forest").update()
            elif (self.realx, self.realy - 1) not in self.forest.areas:
                Area(self.forest, self.realx, self.realy - 1, "forest").update()
            elif (self.realx + 1, self.realy) not in self.forest.areas:
                Area(self.forest, self.realx + 1, self.realy, "forest").update()
            elif (self.realx - 1, self.realy) not in self.forest.areas:
                Area(self.forest, self.realx - 1, self.realy, "forest").update()

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
        self.areas = {}
        self.screenrect = pygame.Rect(camera_x, camera_y, 640, 480)
        pygame.sprite.LayeredUpdates.__init__(self)

    def update(self):
        for s in self.sprites():
            s.update()
        for s in self.sprites():
            s.rect.x -= self.camera_x
            s.rect.y -= self.camera_y
        self.screenrect = pygame.Rect(self.camera_x, self.camera_y, 640, 480)

    def draw(self, surface):
        for spr in sorted(self.sprites(), key=lambda s: s.y):
            surface.blit(spr.image, spr.rect)
