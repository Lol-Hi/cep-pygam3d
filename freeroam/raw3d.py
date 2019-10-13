import pygame
import bet3d as bet

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
GREY = (180, 180, 180)

def cuboid(screen, corner1, corner2, state, colorscheme = "normal", brightness = 1):
    lenX = corner1[0] - corner2[0]
    lenY = corner1[1] - corner2[1]
    lenZ = corner1[2] - corner2[2]

    verticeA = corner1
    verticeB = (verticeA[0] - lenX, verticeA[1], verticeA[2])
    verticeC = (verticeB[0], verticeB[1] - lenY, verticeB[2])
    verticeD = (verticeC[0] + lenX, verticeC[1], verticeC[2])

    verticeE = (verticeA[0], verticeA[1], verticeA[2] - lenZ)
    verticeF = (verticeB[0], verticeB[1], verticeB[2] - lenZ)
    verticeG = (verticeC[0], verticeC[1], verticeC[2] - lenZ)
    verticeH = (verticeD[0], verticeD[1], verticeD[2] - lenZ)

    if state == 1:
        bet._eyeX = bet._OGeyeX
        bet._eyeZ = bet._OGeyeZ
    elif state == 2:
        oldX = bet._OGeyeX
        oldZ = bet._OGeyeZ

        bet._eyeX = oldZ
        bet._eyeZ = -oldX

        verticeA = (verticeA[2], verticeA[1], -verticeA[0])
        verticeB = (verticeB[2], verticeB[1], -verticeB[0])
        verticeC = (verticeC[2], verticeC[1], -verticeC[0])
        verticeD = (verticeD[2], verticeD[1], -verticeD[0])
        verticeE = (verticeE[2], verticeE[1], -verticeE[0])
        verticeF = (verticeF[2], verticeF[1], -verticeF[0])
        verticeG = (verticeG[2], verticeG[1], -verticeG[0])
        verticeH = (verticeH[2], verticeH[1], -verticeH[0])

    elif state == 3:
        bet._eyeX = -bet._OGeyeX
        bet._eyeZ = -bet._OGeyeZ
        # print(bet._eyeX, bet._eyeZ)

        verticeA = (-verticeA[0], verticeA[1], -verticeA[2])
        verticeB = (-verticeB[0], verticeB[1], -verticeB[2])
        verticeC = (-verticeC[0], verticeC[1], -verticeC[2])
        verticeD = (-verticeD[0], verticeD[1], -verticeD[2])
        verticeE = (-verticeE[0], verticeE[1], -verticeE[2])
        verticeF = (-verticeF[0], verticeF[1], -verticeF[2])
        verticeG = (-verticeG[0], verticeG[1], -verticeG[2])
        verticeH = (-verticeH[0], verticeH[1], -verticeH[2])

    elif state == 0:
        oldX = bet._OGeyeX
        oldZ = bet._OGeyeZ

        bet._eyeX = -oldZ
        bet._eyeZ = oldX

        verticeA = (-verticeA[2], verticeA[1], verticeA[0])
        verticeB = (-verticeB[2], verticeB[1], verticeB[0])
        verticeC = (-verticeC[2], verticeC[1], verticeC[0])
        verticeD = (-verticeD[2], verticeD[1], verticeD[0])
        verticeE = (-verticeE[2], verticeE[1], verticeE[0])
        verticeF = (-verticeF[2], verticeF[1], verticeF[0])
        verticeG = (-verticeG[2], verticeG[1], verticeG[0])
        verticeH = (-verticeH[2], verticeH[1], verticeH[0])

    posX = 0
    posY = 0
    if verticeE[2] > bet._eyeZ:
        posX = 1
    elif verticeA[2] < bet._eyeZ:
        posX = -1
    else:
        posX = 0

    if verticeC[1] < bet._eyeY:
        posY = 1
    elif verticeA[1] > bet._eyeY:
        posY = -1
    else:
        posY = 0

    verticeA = bet.Get(verticeA)
    verticeB = bet.Get(verticeB)
    verticeC = bet.Get(verticeC)
    verticeD = bet.Get(verticeD)
    verticeE = bet.Get(verticeE)
    verticeF = bet.Get(verticeF)
    verticeG = bet.Get(verticeG)
    verticeH = bet.Get(verticeH)
    # here

    if state == 1:
        faceRight = [verticeA, verticeB, verticeC, verticeD]
        faceLeft = [verticeE, verticeF, verticeG, verticeH]
        faceBack = [verticeB, verticeC, verticeG, verticeF]
        faceFront = [verticeA, verticeD, verticeH, verticeE]
        faceTop = [verticeA, verticeB, verticeF, verticeE]
        faceBottom = [verticeD, verticeC, verticeG, verticeH]

    elif state == 2:
        faceFront = [verticeE, verticeF, verticeG, verticeH]
        faceBack = [verticeA, verticeB, verticeC, verticeD]
        faceRight = [verticeA, verticeD, verticeH, verticeE]
        faceLeft = [verticeB, verticeC, verticeG, verticeF]
        faceTop = [verticeA, verticeB, verticeF, verticeE]
        faceBottom = [verticeD, verticeC, verticeG, verticeH]

    elif state == 3:
        faceLeft = [verticeA, verticeB, verticeC, verticeD]
        faceRight = [verticeE, verticeF, verticeG, verticeH]
        faceFront = [verticeB, verticeC, verticeG, verticeF]
        faceBack = [verticeA, verticeD, verticeH, verticeE]
        faceTop = [verticeA, verticeB, verticeF, verticeE]
        faceBottom = [verticeD, verticeC, verticeG, verticeH]

    elif state == 0:
        faceFront = [verticeA, verticeB, verticeC, verticeD]
        faceBack = [verticeE, verticeF, verticeG, verticeH]
        faceRight = [verticeB, verticeC, verticeG, verticeF]
        faceLeft = [verticeA, verticeD, verticeH, verticeE]
        faceTop = [verticeA, verticeB, verticeF, verticeE]
        faceBottom = [verticeD, verticeC, verticeG, verticeH]

    tblue = BLUE
    tgreen = GREEN
    tblack = BLACK

    if colorscheme == "black":
        tblue = BLACK
        tgreen = BLACK

    if colorscheme == "white":
        tblue = WHITE
        tgreen = WHITE
        tblack = WHITE

    tblue = tuple([brightness*x for x in tblue])
    tgreen = tuple([brightness * x for x in tgreen])
    tblack = tuple([brightness * x for x in tblack])

    if posX == -1 and posY == -1:
        pygame.draw.polygon(screen, tblue, faceRight)
        pygame.draw.polygon(screen, tgreen, faceFront)
        pygame.draw.polygon(screen, tblack, faceBottom)
    elif posX == 1 and posY == -1:
        pygame.draw.polygon(screen, tblue, faceLeft)
        pygame.draw.polygon(screen, tgreen, faceFront)
        pygame.draw.polygon(screen, tblack, faceBottom)
    elif posX == 1 and posY == 1:
        pygame.draw.polygon(screen, tblue, faceLeft)
        pygame.draw.polygon(screen, tgreen, faceFront)
        pygame.draw.polygon(screen, tblack, faceTop)
    elif posX == -1 and posY == 1:
        pygame.draw.polygon(screen, tblue, faceRight)
        pygame.draw.polygon(screen, tgreen, faceFront)
        pygame.draw.polygon(screen, tblack, faceTop)
    elif posX == 0 and posY == 1:
        pygame.draw.polygon(screen, tgreen, faceFront)
        pygame.draw.polygon(screen, tblack, faceBottom)
    elif posX == 0 and posY == -1:
        pygame.draw.polygon(screen, tgreen, faceFront)
        pygame.draw.polygon(screen, tblack, faceTop)
    elif posX == 1 and posY == 0:
        pygame.draw.polygon(screen, tblue, faceLeft)
        pygame.draw.polygon(screen, tgreen, faceFront)
    elif posX == -1 and posY == 0:
        pygame.draw.polygon(screen, tblue, faceRight)
        pygame.draw.polygon(screen, tgreen, faceFront)
    elif posX == 0 and posY == 0:
        pygame.draw.polygon(screen, tgreen, faceFront)


def sheet(screen, corner1, corner2):
    lenX = corner1[0] - corner2[0]
    lenY = corner1[1] - corner2[1]

    verticeA = corner1
    verticeB = (corner1[0], corner1[1] - lenY, corner1[2])
    verticeC = corner2
    verticeD = (corner2[0], corner2[1] + lenY, corner2[2])

    verticeA = bet.Get(verticeA)
    verticeB = bet.Get(verticeB)
    verticeC = bet.Get(verticeC)
    verticeD = bet.Get(verticeD)

    pygame.draw.polygon(screen, BLACK, [verticeA, verticeB, verticeC, verticeD])