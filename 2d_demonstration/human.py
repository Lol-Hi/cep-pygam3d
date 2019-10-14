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
        self.loc.x = self.loc.x + self.vx * self.game.dt
        if self.loc.x < TILESIZE:
            self.loc.x = TILESIZE
            self.rotate(2*math.pi)
        if self.loc.x > WIDTH-TILESIZE:
            self.loc.x = WIDTH-TILESIZE
            self.rotate(2*math.pi)
        self.loc.z = self.loc.z + self.vz * self.game.dt
        if self.loc.z < TILESIZE:
            self.loc.z = TILESIZE
            self.rotate(2*math.pi)
        if self.loc.z > WIDTH-TILESIZE:
            self.loc.z = WIDTH-TILESIZE
            self.rotate(2*math.pi)
        self.rect.x = self.loc.x
        hit_x = self.collision_check('x')
        self.rect.y = self.loc.z
        hit_z = self.collision_check('z')
        return hit_x or hit_z


    def collision_check(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
                if self.vx > 0:
                    self.loc.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.loc.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.loc.x
                return hits
        if dir == 'z':
            hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
            if hits:
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

class Player(Human):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.calling = False
        self.call_start = 0
        self.call_time = 0
        self.hear_count = 0

    def drawImage(self):
        player = pg.Surface((TILESIZE, TILESIZE))
        player.fill(WHITE)
        player.set_colorkey(WHITE)
        pg.draw.circle(player, RED, (TILESIZE//2, TILESIZE//2), TILESIZE//2)
        return player

    def get_movement(self, keys):
        self.vx, self.vz = 0, 0
        direction = self.front
        if keys[pg.K_a]:
            direction -= math.pi/2
            self.vx, self.vz = PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_d]:
            direction += math.pi/2
            self.vx, self.vz= PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_w]:
            self.vx, self.vz= PLAYER_SPEED, PLAYER_SPEED
        if keys[pg.K_s]:
            direction += math.pi
            self.vx, self.vz= PLAYER_SPEED, PLAYER_SPEED
        self.vx *= math.cos(direction)
        self.vz *= math.sin(direction)

    def get_direction(self, keys):
        if keys[pg.K_LEFT]:
            self.rotate(PLAYER_TURN)
        if keys[pg.K_RIGHT]:
            self.rotate(-PLAYER_TURN)

    def check_calling(self, keys):
        if not(self.game.countdown_start):
            if keys[pg.K_e]:
                self.calling = True
                self.call_start = pg.time.get_ticks()

    def update(self):
        keys = pg.key.get_pressed()
        self.get_direction(keys)
        if self.calling:
            self.call_time = pg.time.get_ticks()-self.call_start
            if self.call_time > MAX_CALL_TIME*1000:
                self.calling = False
                self.game.countdown_start = pg.time.get_ticks()
        else:
            # self.hear_count += 1
            # if self.hear_count%3 == 0:
            #     self.hear()
            self.detect_terrorists()
            self.check_calling(keys)
            self.get_movement(keys)
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
                    break
            if not in_range(phi, self.front-SIGHT_RANGE, self.front+SIGHT_RANGE):
                if dist_person > SIGHT_RADIUS:
                    continue
            if person_visible:
                visible_humans.append(person)
        return visible_obs + visible_humans

    def hear(self):
        l_vol, r_vol = 0, 0
        total_vol = 0
        t_nearby = 0
        for t in self.game.terrorists.sprites():
            t_dist = distance((self.loc.x, self.loc.z), (t.loc.x, t.loc.z))
            t_phi = math.atan2(self.loc.z-t.loc.z, self.loc.x-t.loc.x)
            if t_dist == 0:
                total_vol = 1
                l_vol, r_vol = 1, 1
            elif t_dist <= HEARING_RADIUS:
                t_nearby += 1
                alpha = signed_basic_angle(self.front-t_phi)
                beta = math.pi/2-abs(alpha)
                theta = math.asin(min(1, max(math.sin(beta)*(TILESIZE/2)/t_dist, -1)))
                total_vol = 1-t_dist/HEARING_RADIUS if total_vol == 0 else (1-t_dist/HEARING_RADIUS+total_vol)/2
                softer_vol = 2*(beta-theta)/math.pi
                louder_vol = 2*(beta+theta)/math.pi
                if alpha > 0:
                    l_vol = softer_vol if l_vol == 0 else (l_vol+softer_vol)/2
                    r_vol = louder_vol if r_vol == 0 else (r_vol+louder_vol)/2
                else:
                    l_vol = louder_vol if l_vol == 0 else (l_vol+softer_vol)/2
                    r_vol = softer_vol if r_vol == 0 else (r_vol+softer_vol)/2
    #     try:
    #         self.game.footsteps.set_volume(total_vol/2)
    #         self.game.sound_channel.set_volume(l_vol, r_vol)
    #         self.game.sound_channel.play(self.game.footsteps)
    #     except:
    #         self.game.footsteps2.set_volume(total_vol/2)
    #         self.game.footsteps2.play()

    def detect_terrorists(self):
        for t in self.game.terrorists.sprites():
            t_dist = distance((self.loc.x, self.loc.z), (t.loc.x, t.loc.z))
            if t_dist <= DETECTION_RADIUS:
                angle_diff = self.front - math.atan2(self.loc.z-t.loc.z, self.loc.x-t.loc.x)
                if in_range(angle_diff, -math.pi/4, math.pi/4):
                    arrow_orientation = "down"
                    arrow_x = WIDTH*math.sin(angle_diff)+WIDTH//2
                    arrow_y = HEIGHT
                if in_range(angle_diff, math.pi/4, 3*math.pi/4):
                    arrow_orientation = "right"
                    arrow_x = WIDTH
                    arrow_y = HEIGHT*math.cos(angle_diff)+HEIGHT//2
                if in_range(angle_diff, -3*math.pi/4, -math.pi/4):
                    arrow_orientation = "left"
                    arrow_x = 0
                    arrow_y = HEIGHT*math.cos(-angle_diff)+HEIGHT//2
                if angle_diff < -3*math.pi/4 or angle_diff > 3*math.pi/4:
                    arrow_orientation = "up"
                    arrow_x = -WIDTH*math.sin(-angle_diff)+WIDTH//2
                    arrow_y = MENU_HEIGHT
                self.game.arrows.append([arrow_orientation, arrow_x, arrow_y])


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

    def search_aim(self):
        can_see = self.see()
        if len(can_see) == 0:
            self.move = True
            return
        orig_front = self.front
        min_dist = WIDTH
        to_turn = 0
        person_seen = False
        for person in can_see:
            dist = distance((self.loc.x, self.loc.z), person["pos"])
            if dist < min_dist:
                min_dist = dist
                target = person
                person_seen = True
        if not(person_seen):
            return
        self.front = target["phi"]
        self.shoot_count += 1
        if target["person"].alive() and self.shoot_count <= MAX_SHOOT_TIME:
            if self.shoot_count%SHOOT_INTERVAL == 0:
                self.shoot()
                self.move = False
        else:
            self.shoot_count = 0
            target = None
            self.move = True
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
        for person in good_people:
            phi = math.atan2(
                person.loc.z-self.loc.z,
                person.loc.x-self.loc.x
            )
            self_pos = (self.loc.x, self.loc.z)
            person_pos = (person.loc.x, person.loc.z)
            dist_person = distance(self_pos, person_pos)
            person_visible = True
            if not in_range(phi, self.front-SIGHT_RANGE, self.front+SIGHT_RANGE):
                if dist_person > SIGHT_RADIUS:
                    continue
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
                    break
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