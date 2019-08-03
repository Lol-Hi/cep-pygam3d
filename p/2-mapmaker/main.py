import pygame
import random
pygame.init()

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
PURPLE   = ( 255,   0, 255)

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

num = (2, 2)
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
        rectSurface = pygame.Surface((TILESIZE * 2, TILESIZE * 2))
        rectSurface.fill(PURPLE)
        rectSurface.set_colorkey(PURPLE)
        pygame.draw.rect(screen, self.colour, self.rect, 1)
        # image = rectSurface.convert()
        # print(image)
        # print(self.rect)
        # screen.blit(image, (0,0))

    def change(self, type):
        self.colour = (255, 0, 0) if not self.colour == (255, 0, 0) else (0, 0, 0)

    @staticmethod
    def checkcollision(pos, lastchanged = []):
        if pos[0] < num[0] * TILESIZE and pos[1] < num[1] * TILESIZE:
            # mouseclick event on squares
            x = int(pos[0] / TILESIZE // 1)
            y = int(pos[1] / TILESIZE // 1)
            if not (x, y) == lastchanged:
                grid[y][x].change(1)
                return (x, y)
        return lastchanged

class info:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x * TILESIZE, y * TILESIZE)  # * TILESIZE
        self.rect = pygame.Rect(self.pos, (TILESIZE, TILESIZE))
        self.colour = (0, 0, 0)

    def draw(self, screen):
        rectSurface = pygame.Surface((TILESIZE * 2, TILESIZE * 2))
        rectSurface.fill(PURPLE)
        rectSurface.set_colorkey(PURPLE)
        pygame.draw.rect(screen, self.colour, self.rect, 1)
        # image = rectSurface.convert()
        # print(image)
        # print(self.rect)
        # screen.blit(image, (0,0))

    def change(self, type):
        self.colour = (255, 0, 0) if not self.colour == (255, 0, 0) else (0, 0, 0)

class Ball:
    def __init__(self, x, y, dy):
        self.color = RED
        self.size = 50
        self.image = self.drawImage()
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        self.dy = dy  #define a variable called dy (downwards velocity)

    def drawImage(self):
        ball_surface = pygame.Surface((self.size*2,self.size*2))
        ball_surface.fill(PURPLE)
        ball_surface.set_colorkey(PURPLE)
        pygame.draw.circle(ball_surface, self.color, [self.size, self.size], self.size)
        return ball_surface.convert()

    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def update(self):
        '''
            define a method to update the position of ball
        '''
        self.rect.y += self.dy

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Mapmaker")

done = False

clock = pygame.time.Clock()

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
            # pos = pygame.mouse.get_pos()
            pos = event.pos
            if event.buttons[0]:
                lastchanged = Square.checkcollision(pos, lastchanged)
                print(lastchanged)

    screen.fill(WHITE)
    for row in grid:
        for sq in row:
            sq.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()