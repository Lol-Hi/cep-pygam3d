import pygame
import get

# get.gety(1, 1, 1, 1)  # y, z, g, s


pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PI = 3.141592653

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("test")

done = False
clock = pygame.time.Clock()

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)

    # y = 100
    # z = 200
    # s = 500
    # k = 300
    # g = 1.0 * s / k
    # m_y = s - get.gety(y, z, g, s)
    # # pygame.draw.line(screen, GREEN, [50, m_y], [150, m_y], 5)
    #
    # t1 = 30
    # t2 = 50
    # f = 60
    # l = 400

    constants = get.Data()
    coords = get.Coords()
    m_y = get.newgety(coords, constants)
    m_x1 = get.newgetx(coords, constants)
    coords.x += 1
    m_x2 = get.newgetx(coords, constants)

    #
    # m_x1 = get.getx(t1, f, l)  # t, f, l
    # m_x2 = get.getx(t2, f, l)
    pygame.draw.line(screen, RED, [m_x1, m_y], [m_x2, m_y], 5)

    # for y_offset in range(0, 100, 10):
    #     pygame.draw.line(screen, RED, [0, 10 + y_offset], [100, 110 + y_offset], 5)
    #
    # pygame.draw.rect(screen, BLACK, [20, 20, 250, 100], 2)
    # pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2)
    #
    # pygame.draw.arc(screen, BLACK, [20, 220, 250, 200], 0, PI / 2, 2)
    # pygame.draw.arc(screen, GREEN, [20, 220, 250, 200], PI / 2, PI, 2)
    # pygame.draw.arc(screen, BLUE, [20, 220, 250, 200], PI, 3 * PI / 2, 2)
    # pygame.draw.arc(screen, RED, [20, 220, 250, 200], 3 * PI / 2, 2 * PI, 2)
    #
    # pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)
    #
    # font = pygame.font.SysFont('Calibri', 25, True, False)
    #
    # text = font.render("My text", True, BLACK)
    # screen.blit(text, [250, 250])
    pygame.display.flip()

    clock.tick(60)

pygame.quit()