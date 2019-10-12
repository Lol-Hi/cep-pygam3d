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
    # pointY = vector[1] - _eyeY
    pointY = 0
    pointZ = vector[2] - _eyeZ

    # print(pointX, pointY, pointZ)

    extendX = pointX
    extendY = pointY
    extendZ = 0

    # print(pointX, pointY, pointZ)
    if (extendX, extendY, extendZ) == (0, 0, 0):
        if pointX == 0 and pointZ == 0:
            angle = 0
        else:
            if pointX == 0:
                angle = 90

    else:
        pointVector = pygame.math.Vector3(pointX, pointY, pointZ)
        extendVector = pygame.math.Vector3(extendX, extendY, extendZ)

        # print(pointVector, extendVector)

        # numerator = pointX**2 + _eyeY*pointY + pointZ**2
        # denominator = math.sqrt((pointX**2 + _eyeY**2 + pointZ**2) * (pointX**2 + pointY**2 + pointZ**2))
        # angle = math.degrees(math.acos(numerator / denominator))

        angle = pointVector.angle_to(extendVector)

    # print((pointX, pointY, pointZ))
    # print("Angle:" + str(angle))
    if pointX < 0:
        angle = (180 - angle) % 180

    # print(angle)

    if pointZ < 0:  # TODO: assumes eyeZ = 0
        angle *= -1

    translatedX = (_fovX / 2 + angle) / _fovX * _screenWidth
    # print(translatedX)
    # if pointX < 0:
    #     translatedX *= -1
    # print(translatedX)
    # print(pointX)
    # print(angle)
    return translatedX

def getY(vector):
    pointX = vector[0] - _eyeX
    pointY = vector[1] - _eyeY
    # pointZ = vector[2] - _eyeZ
    pointZ = 0

    extendX = pointX
    extendY = 0
    extendZ = pointZ

    if (extendX, extendY, extendZ) == (0, 0, 0):
        angle = 90
    else:

        pointVector = pygame.math.Vector3(pointX, pointY, pointZ)
        extendVector = pygame.math.Vector3(extendX, extendY, extendZ)

        # print(pointVector, extendVector)

        angle = pointVector.angle_to(extendVector)
    # print(pointX)
    # print(angle)
    if pointX < 0:
        angle = 180 - angle
    # print(angle)

    if pointY > 0:
        angle *= -1

    # print(angle)


    translatedY = (_fovY / 2 + angle) / _fovY * _screenHeight
    # print(translatedY)
    # print(angle)
    return translatedY

def Get(vector):
    # newX = getX(vector)
    # newY = getY(vector)
    # if newX == -1:
    #     return (-1, -1)
    # else:
        return(getX(vector), getY(vector))


# point1 = (10, 8.5, 5)
# getX(point1)
# getY(point1)