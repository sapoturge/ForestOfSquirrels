import pygame
from forestofsquirrels.squirrels import Player
from forestofsquirrels.core.forest import Forest
from forestofsquirrels.trees import Tree


def load_area(area_name, forest=None):
    if forest is None:
        forest = Forest()
    else:
        forest.__init__()
    with open("forestofsquirrels/world/areas/{}.area".format(area_name)) as area:
        lines = [l.strip() for l in area.readlines()]
        width, height = lines[0].split(",")
        forest.width = int(width)
        forest.height = int(height)
        mode = None
        for line in lines[1:]:
            if line == "TREES:":
                mode = "tree"
            elif line == "CONNECTIONS:":
                mode = "connection"
            elif mode == "tree":
                tree, x, y = line.split(",")
                Tree.create_tree(forest, int(x), int(y), tree)
            elif mode == "connection":
                side, area = line.split(",")
                forest.connections[side] = area
    return forest


def run_game():
    pygame.display.set_caption("Forest of Squirrels")
    window = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    forest = load_area("town")
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
                    s.enter_hole(window, clock)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    s.stopleft()
                elif event.key == pygame.K_RIGHT:
                    s.stopright()
                elif event.key == pygame.K_UP:
                    s.stopup()
                elif event.key == pygame.K_DOWN:
                    s.stopdown()

        if s.x < 0:
            if "left" in forest.connections:
                load_area(forest.connections["left"], forest)
                for spr in forest.sprites():
                    if isinstance(spr, Player):
                        spr.kill()
                s.add(forest)
                forest.add(s)
                s.x = forest.width
            else:
                s.x = 0
        elif s.x > forest.width:
            if "right" in forest.connections:
                load_area(forest.connections["right"], forest)
                for spr in forest.sprites():
                    if isinstance(spr, Player):
                        spr.kill()
                s.add(forest)
                forest.add(s)
                s.x = 0
            else:
                s.x = forest.width
        if s.y < 0:
            if "top" in forest.connections:
                load_area(forest.connections["top"], forest)
                for spr in forest.sprites():
                    if isinstance(spr, Player):
                        spr.kill()
                s.add(forest)
                forest.add(s)
                s.y = forest.height
            else:
                s.y = 0
        elif s.y > forest.height:
            if "bottom" in forest.connections:
                load_area(forest.connections["bottom"], forest)
                for spr in forest.sprites():
                    if isinstance(spr, Player):
                        spr.kill()
                s.add(forest)
                forest.add(s)
                s.y = 0
            else:
                s.y = forest.height
        window.fill((0, 128, 0))
        forest.update()
        forest.draw(window)
        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    run_game()
