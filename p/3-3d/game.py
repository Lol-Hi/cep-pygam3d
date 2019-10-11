import pygame
import get

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

    constants = get.Data()
    coords = get.Coords()
    m_ya = get.newgety(coords, constants)
    m_xa1 = get.newgetx(coords, constants)
    coords.x += 1
    m_xa2 = get.newgetx(coords, constants)

    # remember red rectangle supposed to be closer to pldayer than red
    pygame.draw.rect(screen, RED, pygame.Rect(m_xa1, m_ya, m_xa2 - m_xa1, m_ya), 3)

    constants = get.Data()
    coords = get.Coords()
    coords.z -= 1
    m_yb = get.newgety(coords, constants)
    m_xb1 = get.newgetx(coords, constants)
    coords.x += 1
    m_xb2 = get.newgetx(coords, constants)

    # pygame.draw.line(screen, RED, [m_x1, m_y], [m_x2, m_y], 5)
    pygame.draw.rect(screen, BLUE, pygame.Rect(m_xb1, m_yb, m_xb2 - m_xb1, m_yb), 3)

    pygame.draw.line(screen, GREEN, [m_xa1, m_ya], [m_xb1, m_yb], 5)
    pygame.draw.line(screen, GREEN, [m_xa2, m_ya], [m_xb2, m_yb], 5)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
