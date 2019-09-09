import pygame as pg
from settings import *
import math

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, direction, x, z):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.direction = direction
        self.loc = pg.math.Vector3(x, BULLET_HEIGHT, z)
        self.vx, self.vz = 0, 0

    def drawImage(self):
        bullet = pg.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        bullet.fill(DARKGREY)
        return bullet

    def update(self):
        self.vx = math.cos(self.direction)*BULLET_SPEED
        self.vz = math.sin(self.direction)*BULLET_SPEED
        self.loc.x += self.vx * self.game.dt
        self.loc.z += self.vz * self.game.dt
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
        self.checkcollision()

    def checkcollision(self):
        collided_humans = pg.sprite.spritecollide(self, self.game.civilians, True)
        collided_obstacles = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if collided_humans or collided_obstacles:
            self.kill()
        if pg.sprite.collide_rect(self, self.game.player):
            self.kill()
            self.game.player.kill()
            self.playing = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
