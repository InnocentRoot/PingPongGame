import pygame
import sys
import os.path as path
from settings import (
    GAME_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BACKGROUND_VOLUME_LEVEL,
    FPS
)
from config import Config
from menu import Menu
from game import Game
from utils import debug

pygame.init()

clock = pygame.time.Clock()

# Create main window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# We want to play some background music
pygame.mixer.music.load(path.join("sounds", "background-loop.mp3"))
pygame.mixer.music.set_volume(BACKGROUND_VOLUME_LEVEL)
pygame.mixer.music.play(loops=-1)


def start(config):
    debug("===================")
    debug("Start method called")
    debug(f"Difficulty level set to {config.get_difficulty()}")
    debug(f"Mode set to {config.get_mode()}")
    debug(f"Difficulty set to {config.get_difficulty_display_name()}")
    debug("===================")

    game = Game(screen, config, clock)
    game.create_game_components()

    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                debug("Quiting the game...")
                pygame.quit()
                sys.exit()

        pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_UP]:
            game.move_player_up()

        if pressed_key[pygame.K_DOWN]:
            game.move_player_down()

        game.clear_screen()
        game.draw_sprites()
        game.update_screen()

        pygame.display.flip()
        clock.tick(FPS)


config = Config()
menuObject = Menu(screen, config, start)
menuObject.create_menu()

while True:
    debug("Rendering menu")
    clock.tick(FPS)
    menuObject.loop()
    pygame.flip()

pygame.quit()
