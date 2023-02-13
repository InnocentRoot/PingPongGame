"""
Module to store game settings
"""
import pygame

# Window config
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 560
WINDOW_WIDTH_PER2 = WINDOW_WIDTH/2
WINDOW_HEIGHT_PER2 = WINDOW_HEIGHT/2

# Objects config
PADDLE_HEIGHT = 100
PADDLE_WIDTH = 10
BALL_SIZE = 20

GAME_TITLE = "Overkill Ping Pong Game"
FPS = 60

# Mode
GAME_MODE = "DEBUG"  # set to DEBUG to see debug messages

# Font
FONT_SIZE = 10
TIMER_FONT_SIZE = 200

# Colors
WHITE = pygame.Color("white")
GREEN = pygame.Color("green")
BLACK = pygame.Color("black")
RED = pygame.Color("red")
YELLOW = pygame.Color("yellow")
LIGHT_GREY = pygame.Color("grey59")
PURPLE = pygame.Color("purple")

BACKGROUND_COLOR = (237, 231, 225)
BLUE = (0, 115, 251)

# Volume
BACKGROUND_VOLUME_LEVEL = 1  # set to 0 to disable
VOLUME_LEVEL = 1  # set to 0 to disable music
