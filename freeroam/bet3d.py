import pygame
import math

# camera position that is used by processes, altered by camera angle and moving
_eyeX = 3
_eyeY = 17
_eyeZ = 0

# fixed/original camera position, altered only by moving
_OGeyeX = 3
_OGeyeY = 17
_OGeyeZ = 0

# field of view in the x axis (left to right of screen) and the y axis (top to bottom of screen)
_fovX = 150
_fovY = 110

_screenWidth = 400
_screenHeight = 300

def getX(vector):
    # creates a vector along the x-axis that is pushed in/out (by the z value)
    pointX = vector[0] - _eyeX
    pointY = 0
    pointZ = vector[2] - _eyeZ

    # creates a 'basis' vector along the x-axis
    extendX = pointX
    extendY = 0
    extendZ = 0

    if (extendX, extendY, extendZ) == (0, 0, 0):
        # prevents calculation of a zero vector
        # finds the angle between basis vector and altered vector
        if pointX == 0 and pointZ == 0:
            angle = 0
        else:
            if pointX == 0:
                angle = 90

    else:
        pointVector = pygame.math.Vector3(pointX, pointY, pointZ)
        extendVector = pygame.math.Vector3(extendX, extendY, extendZ)
        # finds the angle between basis vector and altered vector
        angle = pointVector.angle_to(extendVector)

    if pointX < 0:
        # the object is behind us
        # if this occurs, the angle is flipped so a modulo is taken
        angle = (180 - angle) % 180

    if pointZ < 0:
        # this means the object is on the left of the screen (vs the right)
        angle *= -1

    # obtains the x coordinate by taking the ratio of the produced angle:fov angle
    # to determine the position of the x coordinate along the screen's x-axis
    translatedX = (_fovX / 2 + angle) / _fovX * _screenWidth
    return translatedX

def getY(vector):
    # idea is the same as getX
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