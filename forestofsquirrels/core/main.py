import pygame
from forestofsquirrels.core.forest import Forest
from forestofsquirrels.trees import Tree


def load_area(area_name):
    forest = Forest()
    with open("forestofsquirrels/world/areas/{}.area".format(area_name)) as area:
        lines = [l.strip() for l in area.readlines()]
        width, height = lines[0].split(",")
        forest.width = int(width)
        forest.height = int(height)
        mode = None
        for line in lines[1:]:
            if line == "TREES:":
                mode = "tree"
            elif mode == "tree":
                print line
                tree, x, y = line.split(",")
                Tree.create_tree(forest, int(x), int(y), tree)
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
        window.fill((0, 128, 0))
        forest.update()
        forest.draw(window)
        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":
    run_game()
