import pygame as pg
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
