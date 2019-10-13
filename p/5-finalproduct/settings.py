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
BLUEGREY = (83,104,120)
YELLOW = (255, 255, 0)
BEIGE = (245, 245, 220)
PURPLE = (128, 0, 128)


# Game settings
WIDTH = 750
HEIGHT = 750
TILESIZE = 15
FPS = 600
TITLE = "Run, Hide, Tell!"
MAX_COUNTDOWN_TIME = 30
MAX_LEVEL = 5

# Font sizes
TITLE_FONTSIZE = 60
NORMAL_FONTSIZE = 25
TINY_FONTSIZE = 12
TITLE_BUFFER = 75
LINE_SPACING = 5
LEFT_INDENT = 100

# Menu settings
MENU_HEIGHT = 35
MENU_BUFFER = (MENU_HEIGHT-NORMAL_FONTSIZE)

# Phone settings
PHONE_WIDTH = 110
PHONE_HEIGHT = 150
PHONESCREEN_WIDTH = 100
PHONESCREEN_HEIGHT = 130
PHONESCREEN_PADDING = 5
PHONE_LEFT = 200
SIDE_BEZEL = (PHONE_WIDTH-PHONESCREEN_WIDTH)/2
TOP_BEZEL = PHONE_HEIGHT-PHONESCREEN_HEIGHT
BUTTON_RADIUS = 10

# Human settings
HUMAN_HEIGHT = 5
SIGHT_RANGE = 5*math.pi/12
SIGHT_RADIUS = 50

# Player settings
PLAYER_TURN = math.pi/50
PLAYER_SPEED = 100
MAX_CALL_TIME = 10
HEARING_RADIUS = 100
DETECTION_RADIUS = 300

# Arrow (terrorist detection) settings
ARROW_LEN = 8
ARROW_WIDTH = 10

# NPC settings
SHOOT_INTERVAL = 2
MAX_SHOOT_TIME = 25
NPC_SPEED = 75

# Bullet settings
BULLET_WIDTH = 2
BULLET_HEIGHT = 2
BULLET_SPEED = 150

# Wall settings
WALL_HEIGHT = 8
