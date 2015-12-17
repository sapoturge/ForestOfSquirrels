import pygame
import os
from forestofsquirrels.world.forest import Forest, Area
from forestofsquirrels import ui
from forestofsquirrels import squirrels


def save(name, squirrel):
    with open("saves/{}.fos".format(name), "w") as savefile:
        savefile.write("0,{},{},{},{}".format(squirrel.x, squirrel.y, int(squirrel.acorn), squirrel.health))


def load(name):
    with open("saves/{}.fos".format(name)) as savefile:
        seed, x, y, acorn, health = savefile.readline().split(",")
        from forestofsquirrels.world import generator
        generator.set_seed(int(seed))
        forest = Forest()
        area = Area(forest, 0, 0, "town")
        area.update()
        x = int(x)
        y = int(y)
        while not area.rect.collidepoint(x, y):
            if area.x > x:
                area = Area(forest, area.realx - 1, area.realy, "forest")
                area.update()
            elif area.x + area.width < x:
                area = Area(forest, area.realx + 1, area.realy, "forest")
                area.update()
            if area.y > y:
                area = Area(forest, area.realx, area.realy - 1, "forest")
                area.update()
            elif area.y + area.height < y:
                area = Area(forest, area.realx, area.realy + 1, "forest")
                area.update()
        forest.player = squirrels.Player(forest, x, y)
        forest.player.acorn = bool(int(acorn))
        forest.player.health = int(health)
    return forest


def show_load_screen():
    import os
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    window = pygame.display.set_mode((640, 480), pygame.NOFRAME)
    window.fill((0, 192, 0))
    pygame.display.update()
    os.environ["SDL_VIDEO_CENTERED"] = ""


def run_game():
    show_load_screen()
    forest = load("save")
    s = forest.player
    ui.create_ui(forest)
    for area in os.walk("forestofsquirrels/world/areas").next()[2]:
        Area.parse_file(area[:-5])
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption("Forest of Squirrels")
    window = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    print forest.sprites()
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
                elif event.key == pygame.K_s:
                    save("save", s)
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
        ui.update()


if __name__ == "__main__":
    run_game()
