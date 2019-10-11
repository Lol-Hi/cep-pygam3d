import pygame as pg
import sys
import os

import random
import math

from settings import *
from human import *
from obstacle import *
from bullet import *
from get import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.game_folder = os.path.dirname(__file__)
        self.assets_folder = os.path.join(self.game_folder, "assets")

        self.footsteps = pg.mixer.Sound(os.path.join(self.assets_folder, "footsteps.wav"))
        self.sound_channel = pg.mixer.Channel(0)

    def new(self):
        self.level = "sample" #for testing purposes, will change later
        self.all_sprites = pg.sprite.Group()
        self.terrorists = pg.sprite.Group()
        self.civilians = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.mapreader()
        self.start_countdown = False
        self.countdown = 0


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
        self.start()
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        self.end()

    def update(self):
        self.all_sprites.update()
        if not(self.player.alive()):
            self.playing = False
            self.win = False
        if self.start_countdown:
            self.countdown += 1
        if self.countdown > COUNTDOWN_TIME:
            self.playing = False
            self.win = True

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

    def start(self):
        pass

    def end(self):
        self.all_sprites.empty()
        self.terrorists.empty()
        self.civilians.empty()
        self.obstacles.empty()

    def quit(self):
        pg.quit()
        sys.exit()

game = Game()

while True:
    game.new()
    game.run()
