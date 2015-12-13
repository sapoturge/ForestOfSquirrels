import pygame
from .uielement import DisplayBar
from .chat import ChatBox
from .health import HealthBar
from .iindicator import AcornIndicator


def create_ui(forest):
    global HUD
    HUD = pygame.sprite.LayeredUpdates()
    DisplayBar(HUD, forest.player)
    ChatBox(HUD, forest.player)
    HealthBar(HUD, forest.player)
    AcornIndicator(HUD, forest.player)


def update():
    HUD.update()
    HUD.draw(pygame.display.get_surface())
    pygame.display.update()
