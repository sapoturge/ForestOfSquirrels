import pygame
from forestofsquirrels.squirrels import Seller, Player
from forestofsquirrels.core.forest import Forest


def run_game():
    window = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    forest = Forest()
    s = Player(forest, 320, 240)
    Seller(forest,25,25)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    s.startleft()
                elif event.key == pygame.K_RIGHT:
                    s.startright()
                elif event.key == pygame.K_UP:
                    s.startup()
                elif event.key == pygame.K_DOWN:
                    s.startdown()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    s.stopleft()
                elif event.key == pygame.K_RIGHT:
                    s.stopright()
                elif event.key == pygame.K_UP:
                    s.stopup()
                elif event.key == pygame.K_DOWN:
                    s.stopdown()
        window.fill((0, 128, 0))
        forest.update()
        forest.draw(window)
        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    run_game()