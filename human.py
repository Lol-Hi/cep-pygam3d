import pygame as pg
from settings import *
from bullet import *

import math

class Human(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.loc = pg.math.Vector2(x*TILESIZE, y*TILESIZE)
        self.vx, self.vy = 0, 0
        self.front = 0

    def drawImage(self):
        pass

    def ai_update(self):
        pass

    def update(self):
        self.ai_update()
        self.loc.x += self.vx * self.game.dt
        self.loc.y += self.vy * self.game.dt
        self.rect.x = self.loc.x
        self.rect.y = self.loc.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(Human):
    def drawImage(self):
        player = pg.Surface((TILESIZE, TILESIZE))
        player.fill(WHITE)
        player.set_colorkey(WHITE)
        pg.draw.circle(player, RED, (TILESIZE//2, TILESIZE//2), TILESIZE//2)
        return player

    def get_keys(self):
        self.vx, self.vy = 0, 0
        direction = self.front
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            direction -= math.pi/2
            self.vx, self.vy = PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            direction += math.pi/2
            self.vx, self.vy = PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vx, self.vy = PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            direction += math.pi
            self.vx, self.vy = PLAYER_SPEED, PLAYER_SPEED
        self.vx *= math.cos(direction)
        self.vy *= math.sin(direction)

    def get_mousepos(self):
        if pg.mouse.get_pressed()[0]:
            movement = pg.mouse.get_rel()[0]
            self.front += movement*PLAYER_TURN

    def update(self):
        self.get_mousepos()
        self.get_keys()
        super().update()

class Terrorist(Human):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.shoot_count = 0

    def drawImage(self):
        terrorist = pg.Surface((TILESIZE, TILESIZE))
        terrorist.fill(WHITE)
        terrorist.set_colorkey(WHITE)
        pg.draw.circle(terrorist, BLACK, (TILESIZE//2, TILESIZE//2), TILESIZE//2)
        return terrorist

    def ai_update(self):
        self.shoot_count += 1
        self.front += math.pi/300
        if self.front >= math.pi:
            self.front -= 2*math.pi
        can_see = self.see()
        if self.shoot_count >= SHOOT_INTERVAL and len(can_see) > 0:
            shoot = True
            for person in can_see:
                shoot &= person["phi"] >= self.front-AIM_RANGE and person["phi"] <= self.front+AIM_RANGE
            if shoot:
                self.shoot()

    def see(self):
        in_range_obs = []
        for obstacle in self.game.obstacles.sprites():
            phi = math.atan2(
                obstacle.loc.y-self.loc.y,
                obstacle.loc.x-self.loc.x
            )
            dist = math.sqrt(
                (obstacle.loc.y-self.loc.y)**2+\
                (obstacle.loc.x-self.loc.x)**2
            )
            if phi >= self.front-SIGHT_RANGE and phi <= self.front+SIGHT_RANGE:
                in_range_obs.append((obstacle, phi, dist))
        good_people = self.game.civilians.sprites() + [self.game.player]
        can_see = []
        for person in good_people:
            phi_p = math.atan2(
                person.loc.y-self.loc.y,
                person.loc.x-self.loc.x
            )
            dist_p = math.sqrt(
                (person.loc.y-self.loc.y)**2+\
                (person.loc.x-self.loc.x)**2
            )
            if phi_p >= self.front-SIGHT_RANGE and phi_p <= self.front+SIGHT_RANGE:
                person_visible = True
                for obstacle, phi_o, dist_o in in_range_obs:
                    person_visible &= not(math.isclose(phi_p, phi_o, rel_tol=0.05) and dist_o < dist_p)
                if person_visible:
                    can_see.append({"person": person, "phi": phi_p, "dist": dist_p})
        return can_see

    def shoot(self):
        bullet_x = self.rect.centerx + (TILESIZE//2 * math.cos(self.front))
        bullet_y = self.rect.centery + (TILESIZE//2 * math.sin(self.front))
        Bullet(self.game, self.front, bullet_x, bullet_y)
        self.shoot_count = 0

class Civilian(Human):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.add(self.game.civilians)

    def drawImage(self):
        civilian = pg.Surface((TILESIZE, TILESIZE))
        civilian.fill(WHITE)
        civilian.set_colorkey(WHITE)
        pg.draw.circle(civilian, YELLOW, (TILESIZE//2, TILESIZE//2), TILESIZE//2)
        return civilian

    def ai_update(self):
        pass
