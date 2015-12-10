import pygame
from forestofsquirrels.world.forest import Forest, Area


def run_game():
    pygame.display.set_caption("Forest of Squirrels")
    window = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    forest = Forest()
    Area(forest, 0, 0, "town")
    s = forest.player
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
                elif event.key == pygame.K_SPACE:
                    s.on_space(window, clock)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    s.stopleft()
                elif event.key == pygame.K_RIGHT:
                    s.stopright()
                elif event.key == pygame.K_UP:
                    s.stopup()
                elif event.key == pygame.K_DOWN:
                    s.stopdown()

        # if s.x < 0:
        #     if "left" in forest.connections:
        #         load_area(forest.connections["left"], forest)
        #         for spr in forest.sprites():
        #             if isinstance(spr, Player):
        #                 spr.kill()
        #         s.add(forest)
        #         forest.add(s)
        #         s.x = forest.width
        #     else:
        #         s.x = 0
        # elif s.x > forest.width:
        #     if "right" in forest.connections:
        #         load_area(forest.connections["right"], forest)
        #         for spr in forest.sprites():
        #             if isinstance(spr, Player):
        #                 spr.kill()
        #         s.add(forest)
        #         forest.add(s)
        #         s.x = 0
        #     else:
        #         s.x = forest.width
        # if s.y < 0:
        #     if "top" in forest.connections:
        #         load_area(forest.connections["top"], forest)
        #         for spr in forest.sprites():
        #             if isinstance(spr, Player):
        #                 spr.kill()
        #         s.add(forest)
        #         forest.add(s)
        #         s.y = forest.height
        #     else:
        #         s.y = 0
        # elif s.y > forest.height:
        #     if "bottom" in forest.connections:
        #         load_area(forest.connections["bottom"], forest)
        #         for spr in forest.sprites():
        #             if isinstance(spr, Player):
        #                 spr.kill()
        #         s.add(forest)
        #         forest.add(s)
        #         s.y = 0
        #     else:
        #         s.y = forest.height
        window.fill((0, 128, 0))
        forest.update()
        forest.draw(window)
        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    run_game()
