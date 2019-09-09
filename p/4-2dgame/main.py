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
        self.level = "sample" #for testing purposes, will change later

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.civilians = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        # #testing only
        # self.player = Player(self, 4, HUMAN_HEIGHT, 5)
        # Obstacle(self, 5, WALL_HEIGHT, 5)
        # Terrorist(self, 10, HUMAN_HEIGHT, 5)
        # Terrorist(self, 12, HUMAN_HEIGHT, 7)
        # Civilian(self, 5, HUMAN_HEIGHT, 12)
        # Civilian(self, 9, HUMAN_HEIGHT, 2)
        # Civilian(self, 13, HUMAN_HEIGHT, 11)
        self.mapreader()


    def mapreader(self):
        with open("./maps/{}.txt".format(self.level)) as mapfile:
            map_width, map_height = mapfile.readline().split(",")
            game_map = mapfile.readline().split(",")
            for row in range(0, int(map_width)):
                for col in range(0, int(map_height)):
                    index = row*int(map_width)+col
                    tile = game_map[index]
                    if tile == "1":
                        self.player = Player(self, row, HUMAN_HEIGHT, col)
                    if tile == "2":
                        Civilian(self, row, HUMAN_HEIGHT, col)
                    if tile == "3":
                        Terrorist(self, row, HUMAN_HEIGHT, col)
                    if tile == "4":
                        Obstacle(self, row, WALL_HEIGHT, col)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        self.end()

    def update(self):
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

    def end(self):
        self.all_sprites.empty()
        self.humans.empty()
        self.obstacles.empty()

    def quit(self):
        pg.quit()
        sys.exit()

game = Game()

while True:
    game.new()
    game.run()
