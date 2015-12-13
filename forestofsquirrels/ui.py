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
        self.rect = pygame.Rect(0, 480 - 20, 640, 20)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((127, 127, 127))


class HealthBar(UIElement):
    def update(self):
        self.image = pygame.Surface((self.squirrel.health * 18, 18)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        for y in range(self.squirrel.health):
            pygame.draw.circle(self.image, (255, 0, 0), (y * 18 + 9, 9), 8)
        self.rect = self.image.get_rect()
        self.rect.bottomright = (640, 480)


class AcornIndicator(UIElement):
    def update(self):
        if self.squirrel.acorn:
            self.image = pygame.image.load("forestofsquirrels/graphics/acorn.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.bottom = 480
        else:
            self.image = pygame.Surface((0, 0))


class ChatBox(UIElement):
    font = pygame.font.Font("freesansbold.ttf", 18)

    def __init__(self, group, squirrel):
        UIElement.__init__(self, group, squirrel)
        self.rect = pygame.Rect(20, 460, 640 - 20 - 8 * 18, 20)
        self.selected = False
        self.text = ""
        self.image = pygame.Surface(self.rect.size)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.selected = True
                else:
                    self.selected = False
                    pygame.event.post(event)
            elif event.type == pygame.KEYDOWN and self.selected:
                if event.key == pygame.K_RETURN:
                    self.squirrel.say(self.text)
                elif event.key == pygame.K_BACKSPACE and len(self.text) > 0:
                    self.text = self.text[:-1]
                elif event.unicode and event.unicode.lower() in "abcdefghijklmnopqrstuvwxyz .?!1234567890,":
                    self.text += event.unicode
                else:
                    pygame.event.post(event)
            else:
                pygame.event.post(event)
        self.image.fill((0, 0, 0))
        self.image.blit(self.font.render(self.text, False, (0, 0, 0), (255, 255, 255)), (1, 1))
        return self.image


def create_ui(forest):
    global HUD
    HUD = pygame.sprite.LayeredUpdates()
    DisplayBar(HUD, forest.player)
    HealthBar(HUD, forest.player)
    AcornIndicator(HUD, forest.player)
    ChatBox(HUD, forest.player)


def update():
    HUD.update()
    HUD.draw(pygame.display.get_surface())
    pygame.display.update()
