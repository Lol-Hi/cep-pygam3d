import math

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (173, 216, 230)
YELLOW = (255, 255, 0)
BEIGE = (245, 245, 220)
PURPLE = (128, 0, 128)


# Game settings
WIDTH = 750
HEIGHT = 750
TILESIZE = 15
FPS = 600
TITLE = "Run, Hide, Tell!"
COUNTDOWN_TIME = 60*1000/FPS

# Human settings
HUMAN_HEIGHT = 5
SIGHT_RANGE = 5*math.pi/12
SIGHT_RADIUS = 50

# Player settings
PLAYER_TURN = math.pi/50
PLAYER_SPEED = 100
CALL_TIME = 15*1000/FPS

# NPC settings
SHOOT_INTERVAL = 2
MAX_SHOOT_TIME = 25
#TERRORIST_ACTIONS = ["move", "move", "move", "left", "right", "right", "left"]
NPC_SPEED = 75

# Bullet settings
BULLET_WIDTH = 2
BULLET_HEIGHT = 2
BULLET_SPEED = 150

# Obstacle settings

# Wall settings
WALL_HEIGHT = 8
