import pygame
import random
import datetime
pygame.init()

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
YELLOW   = ( 255, 255,   0)
PURPLE   = ( 255,   0, 255)

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

num = (3, 3)
size = (SCREEN_WIDTH, SCREEN_HEIGHT)

TILESIZE = 64

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x * TILESIZE, y * TILESIZE)  # * TILESIZE
        self.rect = pygame.Rect(self.pos, (TILESIZE, TILESIZE))
        self.colour = (0, 0, 0)

    def draw(self, screen):
        rectSurface = pygame.Surface((TILESIZE, TILESIZE))
        rectSurface.fill(PURPLE)
        rectSurface.set_colorkey(PURPLE)
        pygame.draw.rect(screen, self.colour, self.rect, 1)
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
            if pos[0] < num[0] * TILESIZE and pos[1] < num[1] * TILESIZE:
                # mouseclick event on squares
                x = int(pos[0] / TILESIZE // 1)
                y = int(pos[1] / TILESIZE // 1)
                if not (x, y) == lastchanged:
                    grid[y][x].change(colour)
                    return (x, y)
        return lastchanged

class Info:
    def __init__(self, y, colour):
        self.y = y
        self.pos = (size[0] - TILESIZE, y * TILESIZE)
        self.rect = pygame.Rect(self.pos, (TILESIZE, TILESIZE))
        self.selected = False
        self.realcolour = colour

    def draw(self, screen):
        rectSurface = pygame.Surface((TILESIZE, TILESIZE))
        rectSurface.fill(PURPLE)
        rectSurface.set_colorkey(PURPLE)
        if self.selected:
            pygame.draw.rect(screen, self.realcolour, self.rect)
        else:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

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
    with open(str(datetime.datetime.now()).replace(":", "-") + ".txt", "w+") as f:
        f.write(str(num[0]) + "," + str(num[1]) + "\n")
        for row in grid:
            for sq in row:
                sqtype = 0
                if sq.colour in infocolours:
                    sqtype = infocolours.index(sq.colour)
                f.write(str(sqtype) + ",")


screen = pygame.display.set_mode(size)

pygame.display.set_caption("Mapmaker")

done = False

clock = pygame.time.Clock()

infos = []
infokeys = ["1", "2", "3", "4"]
infocolours = [RED, BLUE, GREEN, YELLOW]
infoselected = -1
for y, infocolour in enumerate(infocolours):
    infos.append(Info(y, infocolour))
    infokeys[y] = "K_" + infokeys[y]
    infokeys[y] = getattr(pygame, infokeys[y])
# infos[0].change()

grid = []
for y in range(num[1]):
    grid.append([])
    for x in range(num[0]):
        grid[y].append(Square(x, y))

lastchanged = (-1, -1)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            lastchanged = Square.checkcollision(pos)
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            if event.buttons[0]:
                lastchanged = Square.checkcollision(pos, lastchanged)
        if event.type == pygame.KEYDOWN:
            infoselected = Info.checkkey(event.key, infoselected)


    screen.fill(WHITE)
    for row in grid:
        for sq in row:
            sq.draw(screen)
    for info in infos:
        info.draw(screen)
    pygame.display.flip()
    clock.tick(60)

export()
pygame.quit()
