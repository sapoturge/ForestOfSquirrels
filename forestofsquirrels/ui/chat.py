import pygame
from .uielement import UIElement


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
