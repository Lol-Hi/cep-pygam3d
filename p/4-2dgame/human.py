import pygame as pg
from settings import *
from bullet import *

from math_func import *

import math
import random

class Human(pg.sprite.Sprite):
    def __init__(self, game, x, y, z):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.drawImage()
        self.rect = self.image.get_rect()
        self.loc = pg.math.Vector3(x*TILESIZE, y, z*TILESIZE)
        self.rect.x = self.loc.x
        self.rect.y = self.loc.z
        self.vx, self.vz = 0, 0
        self.front = 0

    def drawImage(self):
        pass

    def update(self):
        self.loc.x += self.vx * self.game.dt
        self.loc.z += self.vz * self.game.dt
        self.rect.x = self.loc.x
        hit_x = self.collision_check('x')
        self.rect.y = self.loc.z
        hit_z = self.collision_check('z')
        return hit_x or hit_z


    def collision_check(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
        if hits:
            if dir == 'x':
                if self.vx > 0:
                    self.loc.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.loc.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.loc.x
            if dir == 'z':
                if self.vz > 0:
                    self.loc.z = hits[0].rect.top - self.rect.height
                if self.vz < 0:
                    self.loc.z = hits[0].rect.bottom
                self.vz = 0
                self.rect.y = self.loc.z
        return hits

    def rotate(self, theta):
        self.front += theta
        if self.front > math.pi:
            self.front -= 2*math.pi
        if self.front < -math.pi:
            self.front += 2*math.pi


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # def draw_mark(self):
    #     pg.draw.line(self.game.screen, BLACK, self.rect.topleft, self.rect.bottomright, 10)
    #     pg.draw.line(self.game.screen, BLACK, self.rect.topleft, self.rect.bottomright, 10)


class Player(Human):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.calling = False
        self.call_counter = 0

    def drawImage(self):
        player = pg.Surface((TILESIZE, TILESIZE))
        player.fill(WHITE)
        player.set_colorkey(WHITE)
        pg.draw.circle(player, RED, (TILESIZE//2, TILESIZE//2), TILESIZE//2)
        return player

    def get_keys(self):
        self.vx, self.vz = 0, 0
        direction = self.front
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            direction -= math.pi/2
            self.vx, self.vz = PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            direction += math.pi/2
            self.vx, self.vz= PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vx, self.vz= PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            direction += math.pi
            self.vx, self.vz= PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_e]:
            self.calling = True
        self.vx *= math.cos(direction)
        self.vz *= math.sin(direction)

    def get_mousepos(self):
        if pg.mouse.get_pressed()[0]:
            movement = pg.mouse.get_rel()[0]
            self.front += movement*HUMAN_TURN

    def update(self):
        self.get_mousepos()
        if self.calling:
            self.call_counter += 1
            #print("calling...", self.call_counter)
            if self.call_counter >= CALL_TIME:
                self.calling = False
                self.game.start_countdown = True
        else:
            self.get_keys()
            super().update()

    def see(self):
        visible_obs = []
        for obstacle in self.game.obstacles.sprites():
            signed_dist_x = obstacle.loc.x-self.loc.x
            signed_dist_z = obstacle.loc.z-self.loc.z
            phi = math.atan2(
                signed_dist_z,
                signed_dist_x
            )
            if in_range(phi, self.front-SIGHT_RANGE, self.front+SIGHT_RANGE):
                visible_obs.append(obstacle)
        humans = self.game.civilians.sprites() + self.game.terrorists.sprites()
        visible_humans = []
        for person in humans:
            phi = math.atan2(
                person.loc.z-self.loc.z,
                person.loc.x-self.loc.x
            )
            self_pos = (self.loc.x, self.loc.z)
            person_pos = (person.loc.x, person.loc.z)
            dist_person = distance(self_pos, person_pos)
            person_visible = True
            for obstacle in visible_obs:
                intersect_diag1 = lines_intersect(
                    self_pos,
                    person_pos,
                    obstacle.rect.topleft,
                    obstacle.rect.bottomright
                )
                intersect_diag2 = lines_intersect(
                    self_pos,
                    person_pos,
                    obstacle.rect.topright,
                    obstacle.rect.bottomleft
                )
                if intersect_diag1 or intersect_diag2:
                    person_visible = False
                    #print(self_pos, person_pos, "blocked by {}".format(obstacle.loc))
                    break
            if not in_range(phi, self.front-SIGHT_RANGE, self.front+SIGHT_RANGE):
                if dist_person > SIGHT_RADIUS:
                    #print(self_pos, person_pos, "too far – {}".format(dist_person))
                    continue
            if person_visible:
                visible_humans.append(person)
        return visible_obs + visible_humans


class Terrorist(Human):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.add(self.game.terrorists)
        self.shoot_count = 0
        self.action_count = 0
        self.move = True
        self.front = random.choice([-math.pi/2, 0, math.pi/2, math.pi])

    def drawImage(self):
        terrorist = pg.Surface((TILESIZE, TILESIZE))
        terrorist.fill(WHITE)
        terrorist.set_colorkey(WHITE)
        pg.draw.circle(terrorist, BLACK, (TILESIZE//2, TILESIZE//2), TILESIZE//2)
        return terrorist

    def update(self):
        self.search_aim()
        if self.move:
            self.vx = math.cos(self.front) * NPC_SPEED
            self.vz = math.sin(self.front) * NPC_SPEED
            collision = super().update()
            if collision:
                self.rotate(math.pi)

        # action = TERRORIST_ACTIONS[self.action_count%len(TERRORIST_ACTIONS)]
        # self.action_count += 1
        # shooting = self.search_aim()
        # if shooting:
        #     self.action_count = 0
        #     print(self.loc, target["pos"], self.shoot_count)
        #     return
        # else:
        #     self.vx = math.cos(self.front) * NPC_SPEED
        #     self.vz = math.sin(self.front) * NPC_SPEED
        #     collision = super().update()
        #     if collision:
        #         self.rotate(random.choice([-math.pi/4, math.pi/4]))
        #     if action == "left":
        #         self.rotate(-SIGHT_RANGE)
        #     if action == "right":
        #         self.rotate(SIGHT_RANGE)

    def search_aim(self):
        can_see = self.see()
        #print(self.loc, can_see)
        if len(can_see) == 0:
            #self.rotate(HUMAN_TURN)
            self.move = True
            return None
        #print(self.loc, target)
        orig_front = self.front
        # if target:
        #     self.shoot_count += 1
        #     if target["person"].alive() and self.shoot_count <= MAX_SHOOT_TIME:
        #         #print(target.loc)
        #         self.rotate(self.front-target["phi"])
        #         if self.shoot_count%SHOOT_INTERVAL == 0:
        #             self.shoot()
        #         return "shooting"
        #     else:
        #         self.shoot_count = 0
        #         target = None
        #         #self.rotate(HUMAN_TURN)
        #         print(self.loc, "not shooting", target)
        #         return None

        min_dist = WIDTH
        to_turn = 0
        for person in can_see:
            dist = distance((self.loc.x, self.loc.z), person["pos"])
            if dist < min_dist:
                min_dist = dist
                target = person
        self.front = target["phi"]
        self.shoot_count += 1
        if target["person"].alive() and self.shoot_count <= MAX_SHOOT_TIME:
            #print(self.loc, target["pos"])
            self.rotate(self.front-target["phi"])
            if self.shoot_count%SHOOT_INTERVAL == 0:
                self.shoot()
                self.move = False
        else:
            self.shoot_count = 0
            target = None
            self.move = True
            #self.rotate(HUMAN_TURN)
            #print(self.loc, "not shooting", target)
        self.front = orig_front

    def see(self):
        in_range_obs = []
        for obstacle in self.game.obstacles.sprites():
            phi = math.atan2(
                obstacle.loc.z-self.loc.z,
                obstacle.loc.x-self.loc.x
            )
            if in_range(phi, self.front-SIGHT_RANGE, self.front+SIGHT_RANGE):
                in_range_obs.append(obstacle)
        good_people = self.game.civilians.sprites() + [self.game.player]
        can_see = []
        #print(self.loc, good_people)
        for person in good_people:
            phi = math.atan2(
                person.loc.z-self.loc.z,
                person.loc.x-self.loc.x
            )
            self_pos = (self.loc.x, self.loc.z)
            person_pos = (person.loc.x, person.loc.z)
            dist_person = distance(self_pos, person_pos)
            person_visible = True
            for obstacle in in_range_obs:
                intersect_diag1 = lines_intersect(
                    self_pos,
                    person_pos,
                    obstacle.rect.topleft,
                    obstacle.rect.bottomright
                )
                intersect_diag2 = lines_intersect(
                    self_pos,
                    person_pos,
                    obstacle.rect.topright,
                    obstacle.rect.bottomleft
                )
                if intersect_diag1 or intersect_diag2:
                    person_visible = False
                    #print(self_pos, person_pos, "blocked by {}".format(obstacle.loc))
                    break
            if not in_range(phi, self.front-SIGHT_RANGE, self.front+SIGHT_RANGE):
                if dist_person > SIGHT_RADIUS:
                    #print(self_pos, person_pos, "too far – {}".format(dist_person))
                    continue
            if person_visible:
                can_see.append({"person": person, "phi": phi, "pos": person_pos})
        return can_see

    def shoot(self):
        bullet_x = self.rect.centerx + (TILESIZE//2 * math.cos(self.front))
        bullet_z = self.rect.centery + (TILESIZE//2 * math.sin(self.front))
        Bullet(self.game, self.front, bullet_x, bullet_z)


class Civilian(Human):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.add(self.game.civilians)
        self.front = random.uniform(-math.pi, math.pi)

    def drawImage(self):
        civilian = pg.Surface((TILESIZE, TILESIZE))
        civilian.fill(WHITE)
        civilian.set_colorkey(WHITE)
        pg.draw.circle(civilian, YELLOW, (TILESIZE//2, TILESIZE//2), TILESIZE//2)
        return civilian

    def update(self):
        self.vx = math.cos(self.front) * NPC_SPEED
        self.vz = math.sin(self.front) * NPC_SPEED
        collision = super().update()
        if collision:
            self.rotate(random.uniform(-math.pi, math.pi))
