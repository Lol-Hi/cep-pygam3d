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

#### Sighting mechanism for terrorists

---
## Screenshots and Video

---
## Installation
Firstly, ensure that python3 is installed on your computer.
If not, you can install it [here](https://www.python.org/downloads/).

Secondly, ensure that you have downloaded the following files and folders for
the program
* `assets` – containing the sounds and files used in the program
  * `footprints.wav` – the sound played when the player is near terrorists.
    Obtained from [PacDV](https://www.pacdv.com/sounds/people_sound_effects/footsteps-4.wav)
* `maps` – containing the set ups for the different levels for the game
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
The game may simply be run by running ```main.py```.

When the game runs, a start screen is shown.
Press `ENTER`/`return` to play the game.

The player's movement is controlled by the WASD keys, while the left and right
arrow keys allow the player to turn and look in different directions.
In order to win the level, you will have to press the E key at a safe spot
to call the police, and then wait for the police to arrive.
Note that you will not be able to move when calling the police,
but you can move to other locations after the call when waiting for the police.

You win the game when the police arrive and lose the game when you get shot.
