import pygame as pg
import sys
import os

from settings import *
from human import *
from obstacle import *
from bullet import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        #testing only
        self.player = Player(self, 4, 5)
        Terrorist(self, 10, 5)
        Terrorist(self, 12, 7)
        Civilian(self, 5, 12)
        Civilian(self, 9, 13)
        Civilian(self, 13, 11)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.player.get_mousepos()
        self.player.get_keys()
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

game = Game()

while True:
    game.new()
    game.run()
