import pygame as pg
from settings import *

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, z):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.loc = pg.math.Vector3(x*TILESIZE, y, z*TILESIZE)
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z

    def drawImage(self):
        obstacle = pg.Surface((TILESIZE, TILESIZE))
        obstacle.fill(LIGHTBLUE)
        return obstacle

    def update(self):
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z

    def draw(self, screen):
        screen.draw(self.image, self.rect)

    # def draw_mark(self):
    #     pg.draw.line(self.game.screen, BLACK, self.rect.topleft, self.rect.bottomright, 10)
    #     pg.draw.line(self.game.screen, BLACK, self.rect.topleft, self.rect.bottomright, 10)
