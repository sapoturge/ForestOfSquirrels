import pygame
import random

import forestofsquirrels.squirrels
import forestofsquirrels.trees
from forestofsquirrels.world import generator


class Area(pygame.sprite.Sprite, pygame.sprite.AbstractGroup):
    area_types = {}
    areas = {}

    def __init__(self, forest, x, y, area_name):
        self.forest = forest
        self.connections = {}
        self.realx = x
        self.realy = y
        self.forest.areas[x, y] = self
        pygame.sprite.Sprite.__init__(self, forest)
        pygame.sprite.AbstractGroup.__init__(self)
        if area_name not in Area.area_types:
            Area.parse_file(area_name)
        self.width = Area.area_types[area_name]["width"]
        self.height = Area.area_types[area_name]["height"]
        self.connections = Area.area_types[area_name]["connections"]
        for tx, ty, ttype in Area.area_types[area_name]["trees"]:
            forestofsquirrels.trees.Tree.create_tree(self, tx, ty, ttype)
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
        Area.areas[x, y] = self

    @classmethod
    def parse_file(cls, area_name):
        cls.area_types[area_name] = {"trees": [], "connections": {}}
        with open("forestofsquirrels/world/areas/{}.area".format(area_name)) as area:
            lines = [l.strip() for l in area.readlines()]
            width, height = (int(x) for x in lines[0].split(","))
            mode = None
            for line in lines[1:]:
                if line == "TREES:":
                    mode = "tree"
                elif line == "CONNECTIONS:":
                    mode = "connection"
                elif mode == "tree":
                    tree, tx, ty = line.split(",")
                    if tx == "random":
                        tx = random.randint(0, width)
                    else:
                        tx = int(tx)
                    if ty == "random":
                        ty = random.randint(0, height)
                    else:
                        ty = int(ty)
                    cls.area_types[area_name]["trees"].append((tx, ty, tree))
                elif mode == "connection":
                    side, ctype = line.split(",")
                    cls.area_types[area_name]["connections"][side] = ctype
        cls.area_types[area_name]["width"] = int(width)
        cls.area_types[area_name]["height"] = int(height)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        bigrect = self.forest.screenrect.inflate(1280, 960)
        if not (self.rect.colliderect(bigrect) or bigrect.contains(self.rect)):
            if not self.dead:
                for s in self.sprites():
                    self.forest.remove(s)
                self.dead = True
        elif self.dead:
            for s in self.sprites():
                self.forest.add(s)
            self.dead = False
        if bigrect.contains(self.rect):
            if (self.realx, self.realy + 1) not in self.forest.areas:
                Area(self.forest, self.realx, self.realy + 1,
                     generator.connect(self, self.realx, self.realy + 1, "bottom")).update()
            elif (self.realx, self.realy - 1) not in self.forest.areas:
                Area(self.forest, self.realx, self.realy - 1,
                     generator.connect(self, self.realx, self.realy + 1, "bottom")).update()
            elif (self.realx + 1, self.realy) not in self.forest.areas:
                Area(self.forest, self.realx + 1, self.realy,
                     generator.connect(self, self.realx, self.realy + 1, "bottom")).update()
            elif (self.realx - 1, self.realy) not in self.forest.areas:
                Area(self.forest, self.realx - 1, self.realy,
                     generator.connect(self, self.realx, self.realy + 1, "bottom")).update()
            '''
            if (self.realx + 1, self.realy + 1) not in self.forest.areas:
                Area(self.forest, self.realx + 1, self.realy + 1, "forest").update()
            elif (self.realx - 1, self.realy - 1) not in self.forest.areas:
                Area(self.forest, self.realx - 1, self.realy - 1, "forest").update()
            elif (self.realx + 1, self.realy - 1) not in self.forest.areas:
                Area(self.forest, self.realx + 1, self.realy - 1, "forest").update()
            elif (self.realx - 1, self.realy + 1) not in self.forest.areas:
                Area(self.forest, self.realx - 1, self.realy + 1, "forest").update()
            '''

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
