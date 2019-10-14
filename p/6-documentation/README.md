## Project Title
Run, Hide, Tell!

---
## Description
This is a game which educates its players about the procedures
(Run, Hide and Tell) to follow during a terrorist attack.

---
## Motivations
Since our project has to be for social good, we thought that we could make an
educational game such that people can be more aware about what to do during a
terrorist attack.

---
## Using this branch
Read the write-up first.

2d_demonstration: demonstration of 2d engine

3d_demonstration: demonstration of 3d engine

finalgame: our end product

freeroam: our end product but with death, terrorists and civilians turned off

mapmaker: mapmaker

---
## Build Status
Game mechanics
* Controlling the movement of the player sprite: `Working`
* Controlling the turning of the player sprite: `Working`
* Shooting mechanism for terrorists: `Building`
* Preventing players from walking into walls: `Building`
* Sighting and aiming mechanism for terrorists: `Working`
* Movement of terrorists: `Working`
* Movement of civilians: `Working`
* Hearing mechanism: `Building`
* Calling the police: `Working`

Mapmaker
* Mapmaker to create maps: `Working`

Pseudo-3D representation
* Converting 2d coordinates to 3d coordinates: `Working`
* Creating basic objects and shapes: `Working`
* Creating converging sceneries: `Working`
* Allowing for movement and turning: `Working`
* Converting the 2D representation to a pseudo-3D representation: `Building`

---
## Features

#### 2d to 3d conversion

#### Terrorist detecting mechanism for player
Initially we wanted to play a sound when the player is near the terrorist,
such that the player will know the approximate location of the terrorist.

This is done by looking at the difference in distances to the terrorist from the
left and right edges of the player, using some simple trigonometry.



```python
# in human.py
# is commented out in the 2D code

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
            theta = math.asin(math.sin(beta)*(TILESIZE/2)/t_dist)
            total_vol = 1-t_dist/HEARING_RADIUS if total_vol == 0 else (1-t_dist/HEARING_RADIUS+total_vol)/2
            softer_vol = 2*(beta-theta)/math.pi
            louder_vol = 2*(beta+theta)/math.pi
            if alpha > 0:
                l_vol = softer_vol if l_vol == 0 else (l_vol+softer_vol)/2
                r_vol = louder_vol if r_vol == 0 else (r_vol+louder_vol)/2
            else:
                l_vol = louder_vol if l_vol == 0 else (l_vol+softer_vol)/2
                r_vol = louder_vol if r_vol == 0 else (r_vol+softer_vol)/2
```

However, due to all the processes that were running, pygame's mixer module
kept producing a `NULL tstate` error.
Thus, we had to settle for another method, which is to use markers on the edge
of the screen which will indicate the approximate direction of the terrorists.

The `math.sin()` and `math.cos()` functions shift the markers proportionally to
the angle between the front of the player and the terrorist, while adding
`WIDTH//2` and `HEIGHT//2` ensures that the marker is in the middle when the
terrorist is directly to the front/back/left/right of the player.

```python
# in human.py
class Player(Human):
    # ...
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
```

#### Sighting mechanism for terrorists
Firstly we have to check which civilians the terrorist is able to spot,
and this is done in the `see()` method.
All the obstacles that are in range of the terrorist's sight are collated before
the program checks for the civilians.
If the civilian appears in the range of sight of the terrorist,
he will be detected no matter how far away he is from the terrorist,
but if it is not, those that are outside a certain radius will not be detected.
Afterwards, the program checks if the civilians are blocked by an obstacle
by drawing a line between the terrorist and each detected civilian
and seeing if it intersects the 2 diagonals of each wall.
Those that are not blocked will be returned.

In the `search_aim()` function, if the terrorist does not detect any civilians,
it will simply continue moving.
Or else, it will look for the closest civilian to start shooting.
When it is shooting, it will not move until the person is killed,
or after a certain amount of time which indicates that there is some other
reason that it is not able to shoot the target,
in this case the terrorist will move on and shoot his next target.

```python
# in human.py
class Terrorist(Human):
    # ...
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
```

---
## Screenshots and Video

---
## Installation
Firstly, ensure that python3 is installed on your computer.
If not, you can install it [here](https://www.python.org/downloads/).

Secondly, ensure that you have downloaded the following files and folders for
the program
* `assets` – containing the soundtrack that plays when terrorists are near
  the player
  *  `footsteps.wav` – the soundtrack that plays when terrorists are near the
  player
* `maps` – containing the set ups for the different levels for the game
  * `1.txt` – Level 1
  * `2.txt` – Level 2
  * `3.txt` – Level 3
  * `4.txt` – Level 4
  * `5.txt` – Level 5
* `main.py` – containing the main `Game` class for the program
* `human.py` – containing the `Player`, `Terrorist` and `Civilian` sprites
* `obstacle.py` – containing the `Obstacle` sprite
* `bullet.py` – containing the `Bullet` sprite
* `settings.py` - containing the constants used in the various programs
* `math_func.py` – containing the mathematical functions used in the programs
* `bet.py` – containing the `Get()` function which converts 2D coordinates to
  3D coordinates
* `raw.py` – containing functions to blit pseudo-3D shapes

Last but not least, ensure that you have downloaded pygame version 1.9.5.
If not, you can follow the instructions [here](https://www.pygame.org/wiki/GettingStarted)

---
## How to use?

#### General instructions applicable to both versions
The game may simply be run by running ```main.py```.

When the game runs, a start screen is shown.
Press `ENTER`/`return` to play the game.

The player can move forward and backwards by pressing the `W` and `A` keys
respectively, white turning is achieved with the left and right arrow keys.

#### Instructions in the 2d code
In order to win the game, the player has to press the `E` key to call the police.
The call will take 10 seconds, during which the player will not be able to move,
but he can still be shot by the terrorists.
After the 10 seconds, the police will take 30 seconds to arrive, thus the player
will have to survive during that time.
During this 30 seconds he will be able to move.

You win the game when the police arrive after the 30 seconds
and lose the game when you get shot.
