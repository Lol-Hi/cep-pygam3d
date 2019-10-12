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
_screen = pygame.display.set_mode(_resolution)

def ownDraw(coords, color, surface = _screen):
    pygame.draw.polygon(surface, color, coords)

# TODO: Make design program to draw bird, scale bird, place limb points and export coordinates

class Own:
    # TODO: Automatically scale points in different resolutions
    def __init__(self, coords, color, surface=-1):
        self.ogCoords = coords
        self.currentCoords = []
        for coord in coords:
            self.currentCoords.append(coord)
        self.ogCentre = (0, 0)
        ogCentreX = 0
        ogCentreY = 0
        for point in coords:
            ogCentreX += point[0]
            ogCentreY += point[1]
        ogCentreX /= len(coords)
        ogCentreY /= len(coords)
        self.ogCentre = (ogCentreX, ogCentreY)
        self.currentCentre = (ogCentreX, ogCentreY)
        self.color = color
        self.surface = surface


    def draw(self):
        if self.surface == -1:
            ownDraw(self.currentCoords, self.color)
        else:
            ownDraw(self.currentCoords, self.color, self.surface)

    def rotate(self, angle, pivot = -1, anotherset = None):
        angle %= 360

        if pivot == -1:
            pivot = self.ogCentre

        ihatX = math.cos(math.radians(angle))
        ihatY = math.sin(math.radians(angle))

        # jhatX = -math.cos(math.radians(90 - angle))
        # jhatY = math.sin(math.radians(90 - angle))

        jhatX = -ihatY
        jhatY = ihatX

        for count, point in enumerate(self.ogCoords):
            pointRelative = (point[0] - pivot[0], -point[1] + pivot[1])
            newPointX = (pointRelative[0] * ihatX, pointRelative[0] * ihatY)
            newPointY = (pointRelative[1] * jhatX, pointRelative[1] * jhatY)
            newPoint = (newPointX[0] + newPointY[0], newPointX[1] + newPointY[1])
            self.currentCoords[count] = (newPoint[0] + pivot[0], newPoint[1] + pivot[1])
        # print("current coords: ", self.currentCoords)

    def shift(self, shiftX, shiftY, extraSet = None):
        if not extraSet is None:
            newExtraSet = []
            for point in extraSet:
                newExtraSet.append((point[0] + shiftX, point[1] + shiftY))
            return newExtraSet

        ogCoordsNew = ()
        for coord in self.ogCoords:
            coordNew = (coord[0] + shiftX, coord[1] + shiftY)
            ogCoordsNew += (coordNew,)
        self.ogCoords = ogCoordsNew
        # print(self.ogCoords)

        self.ogCentre = (self.ogCentre[0] + shiftX, self.ogCentre[1] + shiftY)

        for count, coord in enumerate(self.currentCoords):
               self.currentCoords[count] = (coord[0] + shiftX, coord[1] + shiftY)

        self.currentCentre = (self.currentCentre[0] + shiftX, self.currentCentre[1] + shiftY)

        return 1


class Bird:
    def __init__(self, auto=True):
        self.leftWingAngle = 0
        self.rightWingAngle = 0
        self.previousLeftWingState = 0
        self.previousRightWingState = 0
        self.limbs = {
            "leftWing2Body": (0, 0),
            "rightWing2Body": (0, 0)
        }
        if auto:
            self.ConstructBody()
            self.ConstructLeftWing()
            self.ConstructRightWing()

    def ConstructBody(self, coords=None,
                      color=(0, 0, 0)):
        if coords is None:
            coords = ((150, 150), (215, 150), (215, 170), (150, 170))
        self.body = Own(coords, color)

    def ConstructLeftWing(self, coords=None,
                          color=(255, 0, 0), angle = 20):
        if coords is None:
            coords = ((190, 155), (190, 140), (140, 140), (140, 170))
        self.leftWing = Own(coords, color)
        self.leftWingAngle = angle
        self.limbs["leftWing2Body"] = (185, 150)
        self.leftWing.rotate(self.leftWingAngle, self.limbs["leftWing2Body"])

    def ConstructRightWing(self, coords=None,
                          color=(0, 255, 0), angle = 0):
        if coords is None:
            coords = ((190, 155), (190, 140), (140, 140), (140, 170))
        self.rightWing = Own(coords, color)
        self.rightWingAngle = angle
        self.limbs["rightWing2Body"] = (185, 150)
        self.rightWing.rotate(self.rightWingAngle, self.limbs["rightWing2Body"])

    def Draw(self):
        self.body.draw()
        self.leftWing.draw()
        self.rightWing.draw()

    def Move(self):
        shiftX = 1
        shiftY = 1
        newLimbs = self.body.shift(shiftX, shiftY, list(self.limbs.values()))
        for count, limb in enumerate(newLimbs):
            print(limb)
            self.limbs[list(self.limbs.keys())[count]] = limb
        print(self.limbs)
        print("NEW")

        self.body.shift(shiftX, shiftY)
        self.leftWing.shift(shiftX, shiftY)
        self.rightWing.shift(shiftX, shiftY)

    def FlapWings(self):
        if self.leftWingAngle == 0:
            self.leftWingAngle = 1
            self.previousLeftWingState = 0
        elif self.leftWingAngle == 20:
            self.leftWingAngle = 19
            self.previousLeftWingState = 20
        else:
            if self.previousLeftWingState == 20:
                self.leftWingAngle -= 1
            else:
                self.leftWingAngle += 1
        self.leftWing.rotate(self.leftWingAngle, self.limbs["leftWing2Body"])

        # print(self.leftWingAngle)

        if self.rightWingAngle == 0:
            self.rightWingAngle = 1
            self.previousRightWingState = 0
        elif self.rightWingAngle == 20:
            self.rightWingAngle = 19
            self.previousRightWingState = 20
        else:
            if self.previousRightWingState == 20:
                self.rightWingAngle -= 1
            else:
                self.rightWingAngle += 1

        self.rightWing.rotate(self.rightWingAngle, self.limbs["rightWing2Body"])

bird = Bird()

def draw():
    bird.Draw()

def update(state = 0):
    if state == 1:
        bird.FlapWings()
    elif state == 2:
        bird.Move()

pygame.display.set_caption("own")

done = False
clock = pygame.time.Clock()




while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEMOTION:
            update(1)
        if event.type == pygame.KEYDOWN:
            update(2)

    _screen.fill((150, 150, 255))
    draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()