import pygame
import math

pygame.init()


class SpeechBubble(pygame.sprite.Sprite):
    font = pygame.font.Font("freesansbold.ttf", 20)

    def __init__(self, forest, squirrel, message):
        pygame.sprite.Sprite.__init__(self, forest)
        self.message = message
        self.image = self.font.render(message, False, (0, 0, 0), (255, 255, 255))
        self.rect = self.image.get_rect()
        if squirrel.image == squirrel.leftimg:
            self.rect.bottomright = squirrel.rect.topleft
        else:
            self.rect.bottomright = squirrel.rect.topright
        self.updated = 0

    def update(self):
        self.updated += 1
        if self.updated > 60:
            self.kill()


class Squirrel(pygame.sprite.Sprite):
    def __init__(self, forest, x, y):
        self.x = x
        self.y = y
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
            self.y += math.sin(self.hopstep * math.pi / 10) * 20
            self.hopstep += 1
            self.y -= math.sin(self.hopstep * math.pi / 10) * 20
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
        self.rect = pygame.Rect(self.x, self.y, 18, 18)
