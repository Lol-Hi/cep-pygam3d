import pygame
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
            if state == 1:
                if event.key == pygame.K_w:
                    bet._OGeyeX += 1
                if event.key == pygame.K_s:
                    bet._OGeyeX -= 1
            elif state == 2:
                if event.key == pygame.K_w:
                    bet._OGeyeZ += 1
                if event.key == pygame.K_s:
                    bet._OGeyeZ -= 1
            elif state == 3:
                if event.key == pygame.K_w:
                    bet._OGeyeX -= 1
                if event.key == pygame.K_s:
                    bet._OGeyeX += 1
            elif state == 0:
                if event.key == pygame.K_w:
                    bet._OGeyeZ -= 1
                if event.key == pygame.K_s:
                    bet._OGeyeZ += 1
        if event.type == pygame.KEYDOWN:
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

    corner1 = (15, 24, 4)
    corner2 = (21, 23, 2)
    raw.cuboid(_screen, corner1, corner2, state)
    corner1 = (15, 3, 7)
    corner2 = (18, 0, 2)
    raw.cuboid(_screen, corner1, corner2, state)
    corner1 = (15, 8.5, -6)
    corner2 = (18, 5.5, -0)
    raw.cuboid(_screen, corner1, corner2, state)
    corner1 = (6, 17, 3)
    corner2 = (7, 16, 2)
    raw.cuboid(_screen, corner1, corner2, state)

# here
#
    pygame.draw.line(_screen, BLACK, bet.Get((0, 0, -10)), bet.Get((108, 0, -10)))
    pygame.draw.line(_screen, BLACK, bet.Get((0, 30, -10)), bet.Get((108, 30, -10)))

    pygame.draw.line(_screen, BLACK, bet.Get((0, 0, 10)), bet.Get((108, 0, 10)))
    pygame.draw.line(_screen, BLACK, bet.Get((0, 30, 10)), bet.Get((108, 30, 10)))

    pygame.draw.line(_screen, RED, bet.Get((108, 30, -10)), bet.Get((108, 30, 10)))
    pygame.draw.line(_screen, RED, bet.Get((108, 0, -10)), bet.Get((108, 0, 10)))
    pygame.draw.line(_screen, RED, bet.Get((108, 30, -10)), bet.Get((108, 0, -10)))
    pygame.draw.line(_screen, RED, bet.Get((108, 30, 10)), bet.Get((108, 0, 10)))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()