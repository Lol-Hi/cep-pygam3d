import pygame
from settings import *
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, direction, x, z):
        """Initialises attributes specific to the bullet"""
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Surface((TILESIZE, TILESIZE)).convert().get_rect()
        self.direction = direction
        self.loc = pygame.math.Vector3(x, BULLET_HEIGHT, z)
        self.vx, self.vz = 0, 0

    def update(self):
        """Updates the movement of the bullet"""
        self.vx = math.cos(self.direction)*BULLET_SPEED
        self.vz = math.sin(self.direction)*BULLET_SPEED
        self.loc.x += self.vx * self.game.dt
        self.loc.z += self.vz * self.game.dt
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
        self.checkcollision()

    def checkcollision(self):
        """Checks for collisions for the bullet"""
        # If the bullet bumps into a civilian, kill the civilian and destroy the bullet
        collided_humans = pygame.sprite.spritecollide(self, self.game.civilians, True)
        # If the bullet bumps into an obstacle, destroy the bullet
        collided_obstacles = pygame.sprite.spritecollide(self, self.game.obstacles, False)
        if collided_humans or collided_obstacles:
            self.kill()
        # If the bullet bumps into the player, kill the player and destroy the bullet
        if pygame.sprite.collide_rect(self, self.game.player):
            self.kill()
            self.game.player.kill()
