import pygame as pg
from settings import *

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.loc = pg.math.Vector2(x*TILESIZE, y*TILESIZE)

    def drawImage(self):
        obstacle = pg.Surface((TILESIZE, TILESIZE))
        obstacle.fill(LIGHTBLUE)
        return obstacle

    def update():
        self.rect.x = self.loc.x
        self.rect.y = self.loc.y

    def draw(self, screen):
        screen.draw(self.image, self.rect)
