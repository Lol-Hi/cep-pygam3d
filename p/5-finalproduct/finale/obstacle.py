import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, z):
        self.groups = game.all_sprites, game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.loc = pygame.math.Vector3(x*TILESIZE, y, z*TILESIZE)
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
        self.spritetype = "Wall"

    def drawImage(self):
        obstacle = pygame.Surface((TILESIZE, TILESIZE))
        obstacle.fill(LIGHTBLUE)
        return obstacle

    def update(self):
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z

    def draw(self, screen):
        screen.draw(self.image, self.rect)
