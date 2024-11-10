import pygame
import os

pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

width = 1280
height = 720

win = pygame.display.set_mode((width, height))

#colors (r, g, b)
white = (255, 255, 255)
black = (0, 0, 0)
Mint_Green = (172, 255, 172)
Pale_Lavender = (199, 184, 234)
Electric_Blue = (3, 169, 244)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
THE_OTHER_BLUE = (70, 196, 207)
YELLOW = (255, 200, 0)
Electric_Green = (57, 255, 0)
Dark_Red = (139, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)


BGCOLOUR = DARKGREY

TILESIZE = 80
GAPSIZE = 10

MARGIN_X = int((width - (5 * (TILESIZE + GAPSIZE))) / 2)
MARGIN_Y = int((height - (6 * (TILESIZE + GAPSIZE))) / 2)

MARGIN_X1 = int((width - (5 * (TILESIZE + GAPSIZE))) * .15)
MARGIN_Y1 = int((height - (6 * (TILESIZE + GAPSIZE))) * .5)

MARGIN_X2 = int((width - (5 * (TILESIZE + GAPSIZE))) * .85)
MARGIN_Y2 = int((height - (6 * (TILESIZE + GAPSIZE))) * .5)

ROCK_IMAGE = pygame.image.load(os.path.join('Assets', 'Rock.png'))
PLAYER_ROCK_IMAGE = pygame.transform.scale(ROCK_IMAGE, (width*0.4, height*0.4))
OPPONENT_ROCK_IMAGE = pygame.transform.flip(pygame.transform.scale(ROCK_IMAGE, (width*0.4, height*0.4)), True, False)

PAPER_IMAGE = pygame.image.load(os.path.join('Assets', 'Paper.png'))
PLAYER_PAPER_IMAGE = pygame.transform.scale(PAPER_IMAGE, (width*0.4, height*0.4))
OPPONENT_PAPER_IMAGE = pygame.transform.flip(pygame.transform.scale(PAPER_IMAGE, (width*0.4, height*0.4)), True, False)

SCISSOR_IMAGE = pygame.image.load(os.path.join('Assets', 'Scissor.png'))
OPPONENT_SCISSORS_IMAGE = pygame.transform.scale(SCISSOR_IMAGE, (width*0.4, height*0.4))
PLAYER_SCISSORS_IMAGE = pygame.transform.flip(pygame.transform.scale(SCISSOR_IMAGE, (width*0.4, height*0.4)), True, False)



BACKGROUND_TITLE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'TitleBG.png')), (width/6, height*0.37))
RECTANGLE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Win.png')), (width, height))

BLUFF = ["ROCK", "PAPER", "SCISSORS"]

# Create a partition in the middle
BORDER = pygame.Rect(width // 2 - 5, 0, 10, height)

# Load sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'collision.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'smoke_bomb.mp3'))
WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'win!.mp3'))
SPACE_BGM = pygame.mixer.Sound(os.path.join('Assets', 'space_bgm.mp3'))

# Fonts
HEALTH_FONT = pygame.font.SysFont('Consolas', 40)
WINNER_FONT = pygame.font.SysFont('Consolas', 100)

# Game settings
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_width, SPACESHIP_height = 120, 80 
BOX_width = BOX_height = 80

# Custom user events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# Load and scale spaceship images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_width, SPACESHIP_height)), 270)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_width, SPACESHIP_height)), 90)

# Load and scale background image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (width, height))

USER_DATA_DIR = "user_data"
MAX_USERNAME_LENGTH = 15
MAX_PASSWORD_LENGTH = 20

#font 
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Assets/font.ttf", size)