import pygame
import math

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

_resolution = (400, 500)
screen = pygame.display.set_mode(_resolution)

pygame.display.set_caption("birder")

done = False
clock = pygame.time.Clock()

class Mrect:
    def __init__(self, resolution, location, size, color=(0, 0, 0), colorKey=(255, 0, 255)):
        self.location = location
        self.size = size
        self.resolution = resolution
        self.ogsurface = pygame.Surface(self.resolution)
        self.colorKey = colorKey
        self.ogsurface.fill(self.colorKey)
        self.ogsurface.fill(RED)
        self.ogsurface.set_colorkey(self.colorKey)
        self.ogrect = pygame.Rect(self.location, self.size)
        pygame.draw.rect(self.ogsurface, color, self.ogrect)
        self.surface = self.ogsurface
        self.rect = self.surface.get_rect()
        self.center = (self.location[0] + self.size[0] / 2, self.location[1] + self.size[1] / 2)

    def rotate(self, angle):
        rotateBy = angle % 360
        if rotateBy < 90:
            newWidth = self.resolution[0] * math.cos(math.radians(rotateBy))
            newHeight = self.resolution[0] * math.sin(math.radians(rotateBy))
            newGradient = newHeight / newWidth

            newPointX = self.center[0] / self.resolution[0] * newWidth
            # print(newPointX)
            newPointY = newHeight - newGradient * newPointX
            # print(newPointY)

            transUpRight = self.center[1] * math.tan(math.radians(rotateBy))
            transRight = transUpRight * math.cos(math.radians(rotateBy))
            newX = newPointX + transRight

            transDown = transRight / math.tan(math.radians(rotateBy))
            newY = newPointY + transDown
            # print(newX, newY)

            # actual rotation occurs here
            self.surface = pygame.transform.rotate(self.ogsurface, rotateBy)

            adjustX = self.center[0] - newX
            adjustY = self.center[1] - newY
            print(adjustX, adjustY)
            self.rect = self.surface.get_rect()
            newRect = pygame.Rect((self.rect.top + adjustX, self.rect.left + adjustY), self.rect.size)
            self.rect = newRect
        elif rotateBy == 90:
            pass
        elif rotateBy < 180:
            pass
        elif rotateBy == 180:
            pass
        elif rotateBy < 270:
            pass
        elif rotateBy == 270:
            pass
        elif rotateBy < 360:
            pass

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class Bird:
    def __init__(self, resolution, auto=True):
        self.resolution = resolution
        self.leftWingAngle = 90
        if auto:
            self.ConstructBody()
            self.ConstructLeftWing()
            self.ConstructRightWing()

    def ConstructBody(self, location=(150, 150), size=(65, 20), resolution=(-1, -1),
                      color=(0, 0, 0), colorKey=(255, 0, 255)):
        if resolution == (-1, -1):
            resolution = self.resolution
        self.body = Mrect(resolution, location, size, color, colorKey)

    def ConstructLeftWing(self, location=(150, 150), size=(65, 20), resolution=(-1, -1),
                      color=(0, 0, 0), colorKey=(255, 0, 255)):
        if resolution == (-1, -1):
            resolution = self.resolution

        self.leftWing = Mrect(resolution, location, size, color, colorKey)
        self.leftWing.surface = pygame.transform.rotate(self.leftWing.ogsurface, 135)

    def ConstructRightWing(self):
        pass

    def draw(self, screen):
        # self.body.draw(screen)
        self.leftWing.draw(screen)

    def fly(self):
        self.leftWingAngle += 1
        self.leftWing.rotate(self.leftWingAngle)

bird = Bird(_resolution)

def draw():
    bird.draw(screen)

def update():
    bird.fly()


while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # if event.type == pygame.MOUSEMOTION:
            # update()

    screen.fill(BLUE)
    draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()