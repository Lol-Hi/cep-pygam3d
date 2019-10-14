import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, z):
        """Initialises the attributes of the obstacle"""
        self.groups = game.all_sprites, game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = LIGHTBLUE
        self.rect = pygame.Surface((TILESIZE, TILESIZE)).convert().get_rect()
        self.loc = pygame.math.Vector3(x*TILESIZE, y, z*TILESIZE)
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
        self.spritetype = "Wall"
