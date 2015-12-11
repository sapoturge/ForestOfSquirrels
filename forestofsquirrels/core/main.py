import pygame
from forestofsquirrels.world.forest import Forest, Area


def save(name, squirrel):
    with open("saves/{}.fos".format(name), "w") as savefile:
        savefile.write("0,{},{},{},{}".format(squirrel.x, squirrel.y, int(squirrel.acorn), squirrel.health))


def load(name):
    with open("saves/{}.fos".format(name)) as savefile:
        seed, x, y, acorn, health = savefile.readline().split(",")
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
        forest.player.x = x
        forest.player.y = y
        forest.player.climbing = None
        forest.player.z = 0
        forest.player.acorn = bool(int(acorn))
        forest.player.health = int(health)
    return forest


def run_game():
    pygame.display.set_caption("Forest of Squirrels")
    window = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    forest = load("save")
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
