import pygame
import random
pygame.init()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
PURPLE   = ( 255,   0, 255)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Set the width and height of the screen [width, height]
size = (SCREEN_WIDTH, SCREEN_HEIGHT)

class Ball:
    def __init__(self, x, y):
        """
        Create a red ball, radius 50, position with its centre at (x,y)
        """
        self.color = RED
        self.size = 50
        self.image = self.drawImage()
        self.rect = self.image.get_rect()

        # position the drawn ball with its centerx and centery fixed at (x,y)
        self.rect.centerx = x
        self.rect.centery = y

    def drawImage(self):
        """
        Drawing of ball is similar to how it was done in Lesson 2
        except that now it has been moved inside the class, and called when object
        is instantiated
        """
        ball_surface = pygame.Surface((self.size*2,self.size*2))
        ball_surface.fill(PURPLE)
        ball_surface.set_colorkey(PURPLE)
        pygame.draw.circle(ball_surface, self.color, [self.size, self.size], self.size)
        return ball_surface.convert()

    def draw(self,screen):
        """
        This method is responsible in copying the ball image onto the screen
        """
        screen.blit(self.image, self.rect)

screen = pygame.display.set_mode(size)

#setting the window title
pygame.display.set_caption("Ball")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#ball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
ball = Ball(50,50)
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

    screen.fill(BLACK)
    # Draw the ball, passing in the screen as the drawing surface
    ball.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

#Proper shutdown of a Pygame program
pygame.quit()
