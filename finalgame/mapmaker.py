import pygame as pg
import random
import datetime

from settings import *

pg.init()

MAPMAKER_WIDTH = 720
MAPMAKER_HEIGHT = 640

num = (WIDTH//TILESIZE, HEIGHT//TILESIZE)
size = (MAPMAKER_WIDTH, MAPMAKER_HEIGHT)

MAPMAKER_TILESIZE = 12

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x * MAPMAKER_TILESIZE, y * MAPMAKER_TILESIZE)  # * MAPMAKER_TILESIZE
        self.rect = pg.Rect(self.pos, (MAPMAKER_TILESIZE, MAPMAKER_TILESIZE))
        self.colour = (0, 0, 0)

    def draw(self, screen):
        rectSurface = pg.Surface((MAPMAKER_TILESIZE, MAPMAKER_TILESIZE))
        rectSurface.fill(PURPLE)
        rectSurface.set_colorkey(PURPLE)
        pg.draw.rect(screen, self.colour, self.rect, 1)
        # image = rectSurface.convert()
        # print(image)
        # print(self.rect)
        # screen.blit(image, (0,0))

    def change(self, colour):
        # self.colour = (255, 0, 0) if not self.colour == (255, 0, 0) else (0, 0, 0)
        self.colour = colour if not self.colour == colour else (0, 0, 0)

    @staticmethod
    def checkcollision(pos, lastchanged = []):
        if not infoselected == -1:
            colour = infocolours[infoselected]
            if pos[0] < num[0] * MAPMAKER_TILESIZE and pos[1] < num[1] * MAPMAKER_TILESIZE:
                # mouseclick event on squares
                x = int(pos[0] / MAPMAKER_TILESIZE // 1)
                y = int(pos[1] / MAPMAKER_TILESIZE // 1)
                if not (x, y) == lastchanged:
                    grid[y][x].change(colour)
                    return (x, y)
        return lastchanged

class Info:
    def __init__(self, y, colour):
        self.y = y
        self.pos = (size[0] - MAPMAKER_TILESIZE, y * MAPMAKER_TILESIZE)
        self.rect = pg.Rect(self.pos, (MAPMAKER_TILESIZE, MAPMAKER_TILESIZE))
        self.selected = False
        self.realcolour = colour

    def draw(self, screen):
        rectSurface = pg.Surface((MAPMAKER_TILESIZE, MAPMAKER_TILESIZE))
        rectSurface.fill(PURPLE)
        rectSurface.set_colorkey(PURPLE)
        if self.selected:
            pg.draw.rect(screen, self.realcolour, self.rect)
        else:
            pg.draw.rect(screen, (0, 0, 0), self.rect, 1)

    def change(self, infoselected):
        self.selected = not self.selected
        if self.selected:
            infoselected = self.y
            return infoselected
        return infoselected

    @staticmethod
    def checkkey(key, infoselected):
        if key in infokeys:
            return infos[infokeys.index(key)].change(infoselected)

def export():
    #datetime.datetime.now()
    with open("maps/" + str(datetime.datetime.now()).replace(":", "-") + ".txt", "w+") as f:
        f.write(str(num[0]) + "," + str(num[1]) + "\n")
        for row in grid:
            for sq in row:
                sqtype = 0
                if sq.colour in infocolours:
                    sqtype = infocolours.index(sq.colour)
                f.write(str(sqtype) + ",")


screen = pg.display.set_mode(size)

pg.display.set_caption("Mapmaker")

done = False

clock = pg.time.Clock()

infos = []
infokeys = ["0", "1", "2", "3", "4"]
infocolours = [BLACK, RED, YELLOW, PURPLE, LIGHTBLUE]
infoselected = -1
for y, infocolour in enumerate(infocolours):
    infos.append(Info(y, infocolour))
    infokeys[y] = "K_" + infokeys[y]
    infokeys[y] = getattr(pg, infokeys[y])
# infos[0].change()

grid = []
for y in range(num[1]):
    grid.append([])
    for x in range(num[0]):
        grid[y].append(Square(x, y))

lastchanged = (-1, -1)

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = event.pos
            lastchanged = Square.checkcollision(pos)
        if event.type == pg.MOUSEMOTION:
            pos = event.pos
            if event.buttons[0]:
                lastchanged = Square.checkcollision(pos, lastchanged)
        if event.type == pg.KEYDOWN:
            infoselected = Info.checkkey(event.key, infoselected)


    screen.fill(WHITE)
    for row in grid:
        for sq in row:
            sq.draw(screen)
    for info in infos:
        info.draw(screen)
    pg.display.flip()
    clock.tick(60)

export()
pg.quit()