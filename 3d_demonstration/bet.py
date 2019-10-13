import pygame
import math

_eyeX = 3
_eyeY = 17
_eyeZ = 0

_OGeyeX = 3
_OGeyeY = 17
_OGeyeZ = 0

_fovX = 150
_fovY = 110

_screenWidth = 400
_screenHeight = 300

def getX(vector):
    pointX = vector[0] - _eyeX
    pointY = 0
    pointZ = vector[2] - _eyeZ

    extendX = pointX
    extendY = pointY
    extendZ = 0

    if (extendX, extendY, extendZ) == (0, 0, 0):
        if pointX == 0 and pointZ == 0:
            angle = 0
        else:
            if pointX == 0:
                angle = 90

    else:
        pointVector = pygame.math.Vector3(pointX, pointY, pointZ)
        extendVector = pygame.math.Vector3(extendX, extendY, extendZ)

        angle = pointVector.angle_to(extendVector)

    if pointX < 0:
        angle = (180 - angle) % 180

    if pointZ < 0:  # TODO: assumes eyeZ = 0
        angle *= -1

    translatedX = (_fovX / 2 + angle) / _fovX * _screenWidth
    return translatedX

def getY(vector):
    pointX = vector[0] - _eyeX
    pointY = vector[1] - _eyeY
    pointZ = 0

    extendX = pointX
    extendY = 0
    extendZ = pointZ

    if (extendX, extendY, extendZ) == (0, 0, 0):
        angle = 90
    else:

        pointVector = pygame.math.Vector3(pointX, pointY, pointZ)
        extendVector = pygame.math.Vector3(extendX, extendY, extendZ)

        angle = pointVector.angle_to(extendVector)
    if pointX < 0:
        angle = 180 - angle

    if pointY > 0:
        angle *= -1

    translatedY = (_fovY / 2 + angle) / _fovY * _screenHeight
    return translatedY

def Get(vector):
    return(getX(vector), getY(vector))