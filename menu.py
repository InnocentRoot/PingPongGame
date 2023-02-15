""" Menu module """
import sys
import pygame
import pygame_menu
from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BLUE,
    VOLUME_LEVEL,
    FPS
)
from utils import debug


class Menu:
    def __init__(self, surface, config, start):
        self.surface = surface
        self.config = config

        # Menu style
        self.main_menu_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        self.main_menu_theme.set_background_color_opacity(0.7)
        self.main_menu_theme.widget_font = pygame_menu.font.FONT_HELVETICA
        # noqa
        self.main_menu_theme.title_close_button_cursor = \
            pygame_menu.locals.CURSOR_HAND
        self.main_menu_theme.title_background_color = (0, 115, 251)
        self.main_menu_theme.background_color = (171, 183, 183)
        self.main_menu_theme.selection_color = BLUE

        self.start = start  # Function to start the main game
        self.menu = None

    def play_change_sound(self):
        change = pygame.mixer.Sound("sounds/change.mp3")
        change.set_volume(VOLUME_LEVEL)
        pygame.mixer.Sound.play(change)

    def set_difficulty(self, value, difficulty):
        self.play_change_sound()
        self.config.set_difficulty(difficulty)

    def set_mode(self, value, mode):
        self.play_change_sound()
        self.config.set_mode(mode)

    def set_player_name(self, name):
        self.config.set_player_name(name)
        debug(f"Player name change to {self.config.get_player_name()}")

    def start_game(self):
        self.play_change_sound()

        if self.config.get_player_name() == "":
            debug("Player name should not be null", "MENU")
            return self.create_menu()

        debug(f"Current player name {self.config.get_player_name()}")
        debug(f"Player name set to {self.config.get_player_name()}")
        self.start(self.config)

    def exit_game(self):
        debug("Exiting the game, bye !")
        self.play_change_sound()
        sys.exit()

    def add_background(self):
        self.surface.fill((237, 231, 225))

        pygame.draw.line(self.surface,
                         (0, 115, 251),
                         [3, 0],
                         [3, WINDOW_HEIGHT],
                         8)
        pygame.draw.line(self.surface,
                         (0, 115, 251),
                         [0, 3],
                         [WINDOW_WIDTH, 3],
                         8)
        pygame.draw.line(self.surface,
                         (0, 115, 251),
                         [WINDOW_WIDTH - 3, 0],
                         [WINDOW_WIDTH - 3, WINDOW_HEIGHT],
                         8)
        pygame.draw.line(self.surface,
                         (0, 115, 251),
                         [0, WINDOW_HEIGHT - 4],
                         [WINDOW_WIDTH, WINDOW_HEIGHT-4],
                         8)

    # create menu screen and items
    def create_menu(self):
        menu = pygame_menu.Menu(
            title='Jeux de Ping Pong',
            height=WINDOW_HEIGHT * 0.7,
            width=WINDOW_WIDTH * 0.6,
            theme=self.main_menu_theme,
            onclose=self.exit_game
        )

        debug("Menu created, adding buttons")

        menu.add.text_input(
            title='Your name : ',
            maxchar=10,
            default='',
            textinput_id='player_name',
            onchange=self.set_player_name,
            border_color=(0, 115, 251)
        )
        menu.add.selector(
            title='Difficulty : ',
            items=[('Easy', 1), ('Hard', 2), ('Expert', 3)],
            onchange=self.set_difficulty,
        )
        menu.add.button('Play', self.start_game)
        menu.add.button('Quit', self.exit_game)
        menu.add.button('About', self.add_about_menu())

        self.menu = menu

        return menu

    # add about link
    def add_about_menu(self):
        about_menu = pygame_menu.Menu(
            title='About the game',
            height=WINDOW_HEIGHT * 0.7,
            width=WINDOW_WIDTH * 0.6,
            theme=self.main_menu_theme,
            onclose=self.exit_game,
            center_content=False
        )

        about_menu.add.vertical_margin(5)
        about_menu.add.label(
            title='Developer:',
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(5, 1)
        )

        about_menu.add.label(
            title="Developped by github.com/innocentRoot",
            max_char=70,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(29, 1), font_size=20,
            font_color=(255, 255, 255),
            padding=0
        )
        about_menu.add.label(
            title='License:',
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(5, 1)
        )
        about_menu.add.label(
            title="MIT - Do what you want",
            max_char=70,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(29, 1), font_size=20,
            font_color=(255, 255, 255),
            padding=0
        )

        return about_menu

    def loop(self):
        self.menu.mainloop(self.surface, self.add_background, fps_limit=FPS)
