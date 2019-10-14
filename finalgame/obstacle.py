import pygame as pg
from settings import *

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, z):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = LIGHTBLUE
        #self.image = self.drawImage().convert()
        self.rect = pg.Surface((TILESIZE, TILESIZE)).convert().get_rect()
        self.loc = pg.math.Vector3(x*TILESIZE, y, z*TILESIZE)
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
        self.spritetype = "Wall"

    def change(self, color):
        self.color = color
        self.image = self.drawImage().convert()

    def update(self):
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
