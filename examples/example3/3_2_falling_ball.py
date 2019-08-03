import pygame
import random
pygame.init()

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
PURPLE   = ( 255,   0, 255)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

size = (SCREEN_WIDTH, SCREEN_HEIGHT)

class Ball:
    def __init__(self, x, y, dy):
        self.color = RED
        self.size = 50
        self.image = self.drawImage()
        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

        self.dy = dy  #define a variable called dy (downwards velocity)

    def drawImage(self):
        ball_surface = pygame.Surface((self.size*2,self.size*2))
        ball_surface.fill(PURPLE)
        ball_surface.set_colorkey(PURPLE)
        pygame.draw.circle(ball_surface, self.color, [self.size, self.size], self.size)
        return ball_surface.convert()

    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def update(self):
        '''
            define a method to update the position of ball
        '''
        self.rect.y += self.dy

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Falling Ball")

done = False

clock = pygame.time.Clock()

ball = Ball(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,10)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update the ball position
    ball.update()

    screen.fill(BLACK)
    # Draw the ball, passing in the screen as the drawing surface
    ball.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
