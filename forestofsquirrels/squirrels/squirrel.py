import pygame
import math
from forestofsquirrels.trees import Tree

pygame.init()


class SpeechBubble(pygame.sprite.Sprite):
    font = pygame.font.Font("freesansbold.ttf", 20)
    topleft = pygame.image.load("forestofsquirrels/graphics/corner.png")
    topright = pygame.transform.flip(topleft, True, False)
    bottomleft = pygame.transform.flip(topleft, False, True)
    bottomright = pygame.transform.flip(topleft, True, True)

    def __init__(self, forest, squirrel, message):
        pygame.sprite.Sprite.__init__(self, forest)
        self.message = message
        self.squirrel = squirrel
        image = self.font.render(self.message, False, (0, 0, 0), (255, 255, 255))
        self.rect = image.get_rect().inflate(4, 4)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.blit(image, (2, 2))
        self.image.blit(self.topleft, (0, 0))
        self.image.blit(self.topright, (self.rect.width - 4, 0))
        if self.squirrel.image == self.squirrel.leftimg:
            self.rect.bottomright = self.squirrel.rect.topleft
            self.image.blit(self.bottomleft, (0, self.rect.height - 4))
        else:
            self.rect.bottomleft = self.squirrel.rect.topright
            self.image.blit(self.bottomright, (self.rect.width - 4, self.rect.height - 4))
        self.updated = 0
        self.y = self.squirrel.y

    def update(self):
        self.y = self.squirrel.y
        image = self.font.render(self.message, False, (0, 0, 0), (255, 255, 255))
        self.rect = image.get_rect().inflate(4, 4)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.blit(image, (2, 2))
        self.image.blit(self.topleft, (0, 0))
        self.image.blit(self.topright, (self.rect.width - 4, 0))
        if self.squirrel.image == self.squirrel.leftimg:
            self.rect.bottomright = self.squirrel.rect.topleft
            self.image.blit(self.bottomleft, (0, self.rect.height - 4))
        else:
            self.rect.bottomleft = self.squirrel.rect.topright
            self.image.blit(self.bottomright, (self.rect.width - 4, self.rect.height - 4))
        self.updated += 1
        if self.updated > 60:
            self.kill()


class Squirrel(pygame.sprite.Sprite):
    """ Base class for squirrels.
    """

    def __init__(self, forest, x, y):
        self.x = x
        self.y = y
        self.xoffset = 0
        self.yoffset = 0
        self.hoppingLeft = False
        self.hoppingRight = False
        self.hoppingUp = False
        self.hoppingDown = False
        self.goingLeft = False
        self.goingRight = False
        self.goingUp = False
        self.goingDown = False
        self.hopstep = -1
        self.leftimg = pygame.image.load("forestofsquirrels/graphics/squirrel.png").convert_alpha()
        self.rightimg = pygame.transform.flip(self.leftimg, True, False)
        self.image = self.leftimg
        self.rect = self.image.get_rect()
        self.colliderect = self.rect
        self.level = 0
        pygame.sprite.Sprite.__init__(self, forest)
        self.forest = forest

    def startright(self):
        self.goingRight = True
        self.goingLeft = False
        self.image = self.rightimg
        self.hopstep = max(self.hopstep, 0)

    def stopright(self):
        self.goingRight = False

    def startleft(self):
        self.goingLeft = True
        self.goingRight = False
        self.image = self.leftimg
        self.hopstep = max(self.hopstep, 0)

    def stopleft(self):
        self.goingLeft = False

    def startup(self):
        self.goingUp = True
        self.goingDown = False
        self.hopstep = max(self.hopstep, 0)

    def stopup(self):
        self.goingUp = False

    def startdown(self):
        self.goingDown = True
        self.goingUp = False
        self.hopstep = max(self.hopstep, 0)

    def stopdown(self):
        self.goingDown = False

    def say(self, message):
        SpeechBubble(self.forest, self, message)

    def update(self):
        if self.hopstep >= 0:
            if self.hopstep == 0:
                self.hoppingLeft = self.goingLeft
                self.hoppingRight = self.goingRight
                self.hoppingDown = self.goingDown
                self.hoppingUp = self.goingUp
            self.yoffset += math.sin(self.hopstep * math.pi / 10) * 20
            self.hopstep += 1
            self.yoffset -= math.sin(self.hopstep * math.pi / 10) * 20
            if self.hopstep == 10:
                if self.goingRight or self.goingLeft or self.goingUp or self.goingDown:
                    self.hopstep = 0
                else:
                    self.hopstep = -1
                    self.hoppingLeft = False
                    self.hoppingRight = False
                    self.hoppingUp = False
                    self.hoppingDown = False
        if self.hoppingRight:
            self.x += 3
        elif self.hoppingLeft:
            self.x -= 3
        if self.hoppingUp:
            self.y -= 2
        elif self.hoppingDown:
            self.y += 2
        self.colliderect = pygame.Rect(self.x, self.y, 18, 18)
        for tree in filter(lambda s: isinstance(s, Tree), self.forest.sprites()):
            if tree.colliderect.colliderect(self.colliderect):
                if self.hoppingDown:
                    self.colliderect.bottom = tree.colliderect.top
                elif self.hoppingUp:
                    self.colliderect.top = tree.colliderect.bottom
        self.rect = pygame.Rect(self.x + self.xoffset, self.y + self.yoffset, 18, 18)
