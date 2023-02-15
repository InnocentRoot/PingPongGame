import pygame
from random import randint
from settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    VOLUME_LEVEL,
    BALL_SIZE,
    LIGHT_GREY
)
from utils import debug


class Ball(pygame.sprite.Sprite):

    def __init__(self,
                 color,
                 width,
                 height,
                 player,
                 opponent,
                 opponent_paddle,
                 game):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(LIGHT_GREY)
        self.image.set_colorkey(LIGHT_GREY)

        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.velocity_x = randint(8, 8)
        self.velocity_y = randint(-8, 8)

        debug(f"ball velocity:"
              f"X = {self.velocity_x}px,"
              f"Y = {self.velocity_y}px")

        self.rect = self.image.get_rect()
        self.wall_hit_sound = pygame.mixer.Sound("sounds/ball_hit.wav")
        self.wall_hit_sound.set_volume(VOLUME_LEVEL)

        self.lose_sound = pygame.mixer.Sound("sounds/lose.wav")
        self.lose_sound.set_volume(VOLUME_LEVEL)

        self.player = player
        self.opponent = opponent
        self.opponent_paddle = opponent_paddle

        self.game = game

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        self.check_for_walls_collisions()

        # Automatically position the opponent at the center of the ball
        self.position_opponent()

    def bounce(self):
        self.velocity_x = -self.velocity_x
        self.velocity_y = randint(-8, 8)

    def position_opponent(self):
        if self.opponent_paddle.rect.y < self.rect.y:
            self.opponent_paddle.moveDown()

        if self.opponent_paddle.rect.y > self.rect.y:
            self.opponent_paddle.moveUp()

    def check_for_walls_collisions(self):
        # left wall
        if self.rect.x <= 0:
            self.velocity_x = -self.velocity_x
            self.player.increment_score()
            debug(f"Player score 1pt, current score ="
                  f"{self.player.get_score()}", "BALL")
            pygame.mixer.Sound.play(self.wall_hit_sound)
            self.game.restart_game = True
            self.game.set_start_time()

        # right wall
        if self.rect.x >= (WINDOW_WIDTH - 20):
            self.velocity_x = -self.velocity_x
            self.opponent.increment_score()
            debug(
                f"Opponent score 1pt, current score ="
                f"{self.opponent.get_score()}",
                "BALL"
            )
            pygame.mixer.Sound.play(self.wall_hit_sound)
            pygame.mixer.Sound.play(self.lose_sound)
            self.game.restart_game = True
            self.game.set_start_time()

        # top wall
        if self.rect.y <= -1:
            debug(f'Ball at {self.rect.y}')
            self.velocity_y = -self.velocity_y
            pygame.mixer.Sound.play(self.wall_hit_sound)

        # bottom wall WINDOW_HEIGHT  - 12
        if self.rect.y >= WINDOW_HEIGHT - BALL_SIZE:
            debug(f'Ball at {self.rect.y}')
            self.velocity_y = -self.velocity_y
            pygame.mixer.Sound.play(self.wall_hit_sound)
