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
        self.level = 1

    def load_data(self):
        self.game_folder = os.path.dirname(__file__)
        self.assets_folder = os.path.join(self.game_folder, "assets")

        self.title_font = pg.font.Font(None, TITLE_FONTSIZE)
        self.normal_font = pg.font.Font(None, NORMAL_FONTSIZE)
        self.tiny_font = pg.font.Font(None, TINY_FONTSIZE)
        self.normal_linesize = self.normal_font.get_linesize()+LINE_SPACING

        self.footsteps = pg.mixer.Sound(os.path.join(self.assets_folder, "footsteps.wav"))
        self.sound_channel = pg.mixer.Channel(0)
        self.footsteps2 = pg.mixer.music.load(os.path.join(self.assets_folder, "footsteps.wav"))

    def new(self):
        self.start_time = pg.time.get_ticks()
        self.all_sprites = pg.sprite.Group()
        self.terrorists = pg.sprite.Group()
        self.civilians = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.mapreader()
        self.countdown_start = 0
        self.curr_countdown = 0


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

    def update(self):
        self.arrows = []
        self.all_sprites.update()
        if not(self.player.alive()):
            self.playing = False
            self.win = False
        if self.countdown_start:
            self.curr_countdown = pg.time.get_ticks()-self.countdown_start
            if self.curr_countdown > MAX_COUNTDOWN_TIME*1000:
                self.playing = False
                self.win = True
        #print(self.player.front, [obj.loc for obj in self.player.see()])

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
        self.menu()
        if self.player.calling:
            self.phone()
        for arrow in self.arrows:
            self.arrow(arrow)
        pg.display.flip()

    def arrow(self, arrow_lst):
        orientation, x, y = arrow_lst
        p1 = (x, y)
        if orientation == "up":
            p2 = (x+ARROW_WIDTH//2, y+ARROW_LEN)
            p3 = (x-ARROW_WIDTH//2, y+ARROW_LEN)
        elif orientation == "down":
            p2 = (x+ARROW_WIDTH//2, y-ARROW_LEN)
            p3 = (x-ARROW_WIDTH//2, y-ARROW_LEN)
        elif orientation == "left":
            p2 = (x+ARROW_LEN, y+ARROW_WIDTH//2)
            p3 = (x+ARROW_LEN, y-ARROW_WIDTH//2)
        else:
            p2 = (x-ARROW_LEN, y+ARROW_WIDTH//2)
            p3 = (x-ARROW_LEN, y-ARROW_WIDTH//2)
        pg.draw.polygon(self.screen, RED, [p1, p2, p3])

    def menu(self):
        pg.draw.rect(self.screen, BLACK, [0, 0, WIDTH, MENU_HEIGHT])
        level_text = "Level: {}".format(self.level)
        self.screen.blit(
            self.normal_font.render(level_text, True, WHITE),
            (MENU_BUFFER, MENU_BUFFER)
        )
        if self.countdown_start:
            countdown_text = "Time remaining: {}s".format(MAX_COUNTDOWN_TIME-self.curr_countdown//1000)
            self.screen.blit(
                self.normal_font.render(countdown_text, True, WHITE),
                (WIDTH-self.normal_font.size(countdown_text)[0]-MENU_BUFFER, MENU_BUFFER)
            )

    def phone(self):
        pg.draw.rect(self.screen, BLACK, [PHONE_LEFT, HEIGHT-PHONE_HEIGHT, PHONE_WIDTH, PHONE_HEIGHT])
        pg.draw.rect(self.screen, BLUEGREY, [PHONE_LEFT+SIDE_BEZEL, HEIGHT-PHONESCREEN_HEIGHT, PHONESCREEN_WIDTH, PHONESCREEN_HEIGHT])
        curr_calltime = self.player.call_time//1000
        police_text = "999"
        self.screen.blit(
            self.normal_font.render(police_text, True, WHITE),
            (PHONE_LEFT+SIDE_BEZEL+(PHONESCREEN_WIDTH-self.normal_font.size(police_text)[0])//2, HEIGHT-PHONESCREEN_HEIGHT+PHONESCREEN_PADDING)
        )
        calling_text = "00:0{}".format(curr_calltime) if curr_calltime < MAX_CALL_TIME-1 else "call ended"
        self.screen.blit(
            self.tiny_font.render(calling_text, True, WHITE),
            (PHONE_LEFT+SIDE_BEZEL+(PHONESCREEN_WIDTH-self.tiny_font.size(calling_text)[0])//2, HEIGHT-PHONESCREEN_HEIGHT+self.normal_linesize)
        )
        for i in range(0, 9):
            curr_x = int(PHONE_LEFT+SIDE_BEZEL+(i%3+1)*PHONESCREEN_WIDTH//4)
            curr_z = HEIGHT-PHONESCREEN_HEIGHT+PHONESCREEN_PADDING+2*self.normal_linesize+i//3*(self.normal_linesize)
            pg.draw.circle(self.screen, WHITE, (curr_x, curr_z), BUTTON_RADIUS, 1)
            self.screen.blit(
                self.tiny_font.render(str(i+1), True, WHITE),
                (curr_x-self.tiny_font.size(str(i+1))[0]/4, curr_z-self.tiny_font.get_linesize()/2)
            ) # Don't know why we need to divide by 4 instead of 2, but it fits better this way
        pg.draw.circle(self.screen, RED, (int(PHONE_LEFT+SIDE_BEZEL+PHONESCREEN_WIDTH//2), HEIGHT), BUTTON_RADIUS)

    def start(self):
        self.screen.fill(LIGHTBLUE)
        self.title_font.set_bold(True)
        self.screen.blit(
            self.title_font.render(TITLE, False, BLACK),
            ((WIDTH-self.title_font.size(TITLE)[0])//2, TITLE_BUFFER)
        )
        self.title_font.set_bold(False)
        self.normal_font.set_underline(True)
        self.screen.blit(
            self.normal_font.render("Instructions", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER)
        )
        self.screen.blit(
            self.normal_font.render("Controls", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+5*LINE_SPACING+4*self.normal_linesize)
        )
        self.normal_font.set_underline(False)
        self.screen.blit(
            self.normal_font.render("1. RUN away from the terrorists", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+self.normal_linesize)
        )
        self.screen.blit(
            self.normal_font.render("2. Find a safe place to HIDE", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+2*self.normal_linesize)
        )
        self.screen.blit(
            self.normal_font.render("3. Press <E> to call the police to TELL them about the situation", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+3*self.normal_linesize)
        )
        self.screen.blit(
            self.normal_font.render("WASD: Movement", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+5*LINE_SPACING+5*self.normal_linesize)
        )
        self.screen.blit(
            self.normal_font.render("Left and Right arrow keys: Turning", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+5*LINE_SPACING+6*self.normal_linesize)
        )
        self.screen.blit(
            self.normal_font.render("E: Call the police (Tell)", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+5*LINE_SPACING+7*self.normal_linesize)
        )
        self.normal_font.set_italic(True)
        self.screen.blit(
            self.normal_font.render("Note – When calling the police, your character will NOT be able to move", False, BLACK),
            (LEFT_INDENT, 2*TITLE_BUFFER+5*LINE_SPACING+8*self.normal_linesize)
        )
        self.normal_font.set_italic(False)
        instruction = "Press <ENTER>/<RETURN> to start game"
        self.screen.blit(
            self.normal_font.render(instruction, False, BLACK),
            ((WIDTH-self.normal_font.size(instruction)[0])//2, HEIGHT-TITLE_BUFFER)
        )
        pg.display.flip()
        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_RETURN:
                    return

    def end(self):
        self.all_sprites.empty()
        self.terrorists.empty()
        self.civilians.empty()
        self.obstacles.empty()
        if self.player.alive:
            self.player.kill()

        self.end_time = pg.time.get_ticks()
        time_elapsed = (self.end_time-self.start_time)//1000
        time_text = "Time taken: {} min {} s".format(time_elapsed//60, time_elapsed%60)
        level_text = "Current level: {}".format(self.level)
        self.title_font.set_bold(True)
        if self.win:
            if self.level == MAX_LEVEL:
                self.screen.fill(YELLOW)
                win_text = "You completed all the levels!"
                instruction = "Press <ENTER>/<RETURN> to restart"
            else:
                self.screen.fill(WHITE)
                win_text = "You Won!"
                instruction = "Press <ENTER>/<RETURN> to move on to the next level"
            self.screen.blit(
                self.title_font.render(win_text, False, BLACK),
                ((WIDTH-self.title_font.size(win_text)[0])//2, TITLE_BUFFER)
            )
            self.screen.blit(
                self.normal_font.render(level_text, False, BLACK),
                ((WIDTH-self.normal_font.size(level_text)[0])//2, 2*TITLE_BUFFER)
            )
            self.screen.blit(
                self.normal_font.render(time_text, False, BLACK),
                ((WIDTH-self.normal_font.size(time_text)[0])//2, 2*TITLE_BUFFER+self.normal_linesize)
            )
            self.screen.blit(
                self.normal_font.render(instruction, False, BLACK),
                ((WIDTH-self.normal_font.size(instruction)[0])//2, HEIGHT-TITLE_BUFFER)
            )
            pg.display.flip()
            while True:
                event = pg.event.wait()
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_RETURN:
                        if self.level == MAX_LEVEL:
                            self.level = 1
                        else:
                            self.level += 1
                        return
        else:
            self.screen.fill(BLACK)
            lose_text = "You Died"
            instruction = "Press <ENTER>/<RETURN> to restart"
            self.screen.blit(
                self.title_font.render(lose_text, False, WHITE),
                ((WIDTH-self.title_font.size(lose_text)[0])//2, TITLE_BUFFER)
            )
            self.screen.blit(
                self.normal_font.render(level_text, False, WHITE),
                ((WIDTH-self.normal_font.size(level_text)[0])//2, 2*TITLE_BUFFER)
            )
            self.screen.blit(
                self.normal_font.render(time_text, False, WHITE),
                ((WIDTH-self.normal_font.size(time_text)[0])//2, 2*TITLE_BUFFER+self.normal_linesize)
            )
            self.screen.blit(
                self.normal_font.render(instruction, False, WHITE),
                ((WIDTH-self.normal_font.size(instruction)[0])//2, HEIGHT-TITLE_BUFFER)
            )
            pg.display.flip()
            while True:
                event = pg.event.wait()
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_RETURN:
                        self.level = 1
                        return
        self.title_font.set_bold(True)

    def quit(self):
        pg.quit()
        sys.exit()

game = Game()

game.start()
while True:
    game.new()
    game.run()
    game.end()
