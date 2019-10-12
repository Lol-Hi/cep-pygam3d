import pygame
import get
import bet
import raw

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
GREY = (180, 180, 180)

size = (400, 300)
_screen = pygame.display.set_mode(size)

pygame.display.set_caption("test")

done = False
clock = pygame.time.Clock()

state = 1
# 0 - left, 1 - straight, 2 - right, 3 - back

while not done:
    print(state)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                bet._OGeyeX += 1
            if event.key == pygame.K_s:
                bet._OGeyeX -= 1
        if event.type == pygame.KEYDOWN:
            # oldX = bet._eyeX
            # oldZ = bet._eyeZ
            # bet._eyeX = -oldZ
            # bet._eyeZ = oldX
            if event.key == pygame.K_a:
                state = (state - 1) % 4
            if event.key == pygame.K_d:
                state = (state + 1) % 4


    # print("X:" + str(bet._eyeX))

    _screen.fill(WHITE)

    # here

    point7 = (108, 21, -5)
    p7 = bet.Get(point7)

    point8 = (108, 21, 5)
    p8 = bet.Get(point8)

    point9 = (108, 0, -5)
    p9 = bet.Get(point9)

    point10 = (108, 0, 5)
    p10 = bet.Get(point10)


    pygame.draw.polygon(_screen, BLUE, [p7, p8, p10, p9])
# here

    # a = bet.Get((15, 3, 7))
    # b = bet.Get((18, 3, 7))
    # c = bet.Get((15, 0, 7))
    # d = bet.Get((18, 0, 7))
    #
    # e = bet.Get((15, 3, 2))
    # f = bet.Get((18, 3, 2))
    # g = bet.Get((15, 0, 2))
    # h = bet.Get((18, 0, 2))

# here
    # floor
    pygame.draw.polygon(_screen, GRAY,
                        [bet.Get((0, 0, -10)), bet.Get((0, 0, 10)), bet.Get((108, 0, 10)), bet.Get((108, 0, -10))])
    # ceiling
    pygame.draw.polygon(_screen, GRAY,
                        [bet.Get((0, 30, -10)), bet.Get((0, 30, 10)), bet.Get((108, 30, 10)), bet.Get((108, 30, -10))])
    # lWall
    pygame.draw.polygon(_screen, GREY,
                        [bet.Get((0, 0, -10)), bet.Get((0, 30, -10)), bet.Get((108, 30, -10)), bet.Get((108, 0, -10))])
    # rWall
    pygame.draw.polygon(_screen, GREY,
                        [bet.Get((0, 30, 10)), bet.Get((0, 0, 10)), bet.Get((108, 0, 10)), bet.Get((108, 30, 10))])

    # here

    # first 3d object
    # pygame.draw.polygon(_screen, RED, [a, b, d, c])
    # pygame.draw.polygon(_screen, GREEN, [a, c, g, e])
    # pygame.draw.polygon(_screen, BLUE, [a, b, f, e])
    # pygame.draw.polygon(_screen, BLACK, [e, f, h, g])
    corner1 = (15, 24, 4)
    corner2 = (21, 23, 2)
    raw.cuboid(_screen, corner1, corner2, state)
    corner1 = (15, 3, 7)
    corner2 = (18, 0, 2)
    raw.cuboid(_screen, corner1, corner2, state)
    corner1 = (15, 8.5, -6)
    corner2 = (18, 5.5, -0)
    raw.cuboid(_screen, corner1, corner2, state)
    # corner1 = (15, 20, -6)
    # corner2 = (18, 17, -0)
    corner1 = (6, 17, 3)
    corner2 = (7, 16, 2)
    raw.cuboid(_screen, corner1, corner2, state)

# here
#
#     pygame.draw.line(_screen, BLACK, bet.Get((0, 0, -10)), bet.Get((108, 0, -10)))
#     pygame.draw.line(_screen, BLACK, bet.Get((0, 30, -10)), bet.Get((108, 30, -10)))
#
#     pygame.draw.line(_screen, BLACK, bet.Get((0, 0, 10)), bet.Get((108, 0, 10)))
#     pygame.draw.line(_screen, BLACK, bet.Get((0, 30, 10)), bet.Get((108, 30, 10)))
#
#     pygame.draw.line(_screen, RED, bet.Get((108, 30, -10)), bet.Get((108, 30, 10)))
#     pygame.draw.line(_screen, RED, bet.Get((108, 0, -10)), bet.Get((108, 0, 10)))
#     pygame.draw.line(_screen, RED, bet.Get((108, 30, -10)), bet.Get((108, 0, -10)))
#     pygame.draw.line(_screen, RED, bet.Get((108, 30, 10)), bet.Get((108, 0, 10)))

    # here

    # pygame.draw.polygon(_screen, GREEN, )

    # pygame.draw.line(_screen, BLACK, p1, p2)
    # pygame.draw.line(_screen, BLACK, pA, pB)
    # pygame.draw.line(_screen, RED, p3, p4)
    # pygame.draw.line(_screen, RED, p5, p6)
    #
    # pygame.draw.polygon(_screen, BLACK, [p1, p2, pB, pA])
    # pygame.draw.polygon(_screen, RED, [p3, p4, p6, p5])

    # constants = get.Data()
    # coords = get.Coords()
    # m_ya = get.newgety(coords, constants)
    # m_xa1 = get.newgetx(coords, constants)
    # coords.x += 1
    # m_xa2 = get.newgetx(coords, constants)
    #
    # # remember red rectangle supposed to be closer to pldayer than red
    # pygame.draw.rect(screen, RED, pygame.Rect(m_xa1, m_ya, m_xa2 - m_xa1, m_ya), 3)
    #
    # constants = get.Data()
    # coords = get.Coords()
    # coords.z -= 1
    # m_yb = get.newgety(coords, constants)
    # m_xb1 = get.newgetx(coords, constants)
    # coords.x += 1
    # m_xb2 = get.newgetx(coords, constants)
    #
    # # pygame.draw.line(screen, RED, [m_x1, m_y], [m_x2, m_y], 5)
    # pygame.draw.rect(screen, BLUE, pygame.Rect(m_xb1, m_yb, m_xb2 - m_xb1, m_yb), 3)
    #
    # pygame.draw.line(screen, GREEN, [m_xa1, m_ya], [m_xb1, m_yb], 5)
    # pygame.draw.line(screen, GREEN, [m_xa2, m_ya], [m_xb2, m_yb], 5)



    pygame.display.flip()

    clock.tick(60)

pygame.quit()