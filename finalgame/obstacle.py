import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, z):
        self.groups = game.all_sprites, game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = LIGHTBLUE
        self.image = self.drawImage().convert()
        self.rect = self.image.get_rect()
        self.loc = pygame.math.Vector3(x*TILESIZE, y, z*TILESIZE)
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
        self.spritetype = "Wall"


    def drawImage(self):
        obstacle = pygame.Surface((TILESIZE, TILESIZE))
        obstacle.fill(self.color)
        return obstacle

    def change(self, color):
        self.color = color
        self.image = self.drawImage().convert()

    def update(self):
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z

    def draw(self, screen):
        screen.draw(self.drawImage().convert(), self.rect)
