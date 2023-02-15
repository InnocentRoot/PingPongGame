""" Module for game initialization """
import pygame
from paddle import Paddle
from ball import Ball
from player import Player
from opponent import Opponent
from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_HEIGHT_PER2,
    WINDOW_WIDTH_PER2,
    VOLUME_LEVEL,
    PURPLE,
    BALL_SIZE,
    BACKGROUND_COLOR,
    BLACK,
    RED,
    BLUE,
    GREEN,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    FONT_SIZE,
    TIMER_FONT_SIZE
)
from utils import debug


class Game:
    def __init__(self, screen, config, clock):
        self.screen = screen
        self.config = config
        self.clock = clock

        self.player = Player(self.config.get_player_name(), 0)
        self.opponent = Player("Computer", 0)

        # Create the player paddle
        self.player_paddle = Paddle(GREEN, PADDLE_WIDTH, PADDLE_HEIGHT)

        # Create the opponent paddle
        self.opponent_paddle = Opponent(RED, PADDLE_WIDTH, PADDLE_HEIGHT, self)

        # Create the ball
        self.ball = Ball(
            PURPLE, BALL_SIZE,
            BALL_SIZE,
            self.player,
            self.opponent,
            self.opponent_paddle,
            self
        )

        # Sprites
        self.paddle_group = pygame.sprite.Group()
        self.ball_sprite = pygame.sprite.GroupSingle()

        # Fonts
        self.font_normal = \
            pygame.font.Font('fonts/gasalt.regular.ttf', 26)

        self.font_big = pygame.font.Font('fonts/gasalt.regular.ttf', 34)
        self.font_timer = pygame.font.Font(
            'fonts/gasalt.regular.ttf',
            TIMER_FONT_SIZE
        )

        # Sound
        self.ball_hit_sound = pygame.mixer.Sound("sounds/ball_hit.wav")
        self.wall_hit_sound = pygame.mixer.Sound("sounds/banging-to-wall.mp3")

        self.ball_hit_sound.set_volume(VOLUME_LEVEL)
        self.wall_hit_sound.set_volume(VOLUME_LEVEL)

        self.restart_game = False
        self.timer_value = None
        self.start_time = None

    def create_game_components(self):
        self.display_fps()
        self.draw_players_scores()
        self.draw_middle_line()
        self.ball_sprite_rect()
        self.player_paddle_rect()
        self.opponent_paddle_rect()
        self.draw_sprites()

    def ball_sprite_rect(self):
        self.ball.rect.x = WINDOW_WIDTH_PER2 - BALL_SIZE/2
        self.ball.rect.y = WINDOW_HEIGHT_PER2 - BALL_SIZE/2
        self.ball_sprite.add(self.ball)

    def player_paddle_rect(self):
        self.player_paddle.rect.x = 680
        self.player_paddle.rect.y = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.paddle_group.add(self.player_paddle)

    def opponent_paddle_rect(self):
        self.opponent_paddle.rect.x = 10
        self.opponent_paddle.rect.y = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.paddle_group.add(self.opponent_paddle)

    def clear_screen(self):
        self.screen.fill(BACKGROUND_COLOR)

    def draw_sprites(self):
        self.paddle_group.draw(self.screen)
        self.ball_sprite.draw(self.screen)

    def set_start_time(self):
        self.start_time = pygame.time.get_ticks()
        debug(f"Start timer set to {self.start_time}")

    # Update Redraw all visual elements to screen
    def update_screen(self):
        if self.restart_game:
            self.draw_scene_delimitor()
            self.draw_players_scores()
            self.draw_middle_line()

            # Position the ball at the center
            self.ball.rect.x = WINDOW_WIDTH/2 - BALL_SIZE/2
            self.ball.rect.y = WINDOW_HEIGHT/2 - BALL_SIZE/2

            elapsed_seconds = (pygame.time.get_ticks() - self.start_time)/1000

            if elapsed_seconds < 1:
                timer = self.font_timer.render('3...', 1, BLUE)
                self.screen.blit(timer,
                                 (WINDOW_WIDTH/2 - timer.get_width()/2,
                                  WINDOW_HEIGHT/2 - 200)
                                 )

            elif 1 < elapsed_seconds < 2:
                timer = self.font_timer.render('2...', 1, BLUE)
                self.screen.blit(timer,
                                 (WINDOW_WIDTH/2 - timer.get_width()/2 + 30,
                                  WINDOW_HEIGHT/2 - 200)
                                 )
            elif 2 < elapsed_seconds < 3:
                timer = self.font_timer.render('1...', 1, BLUE)
                self.screen.blit(timer,
                                 (WINDOW_WIDTH/2 - timer.get_width()/2 + 40,
                                  WINDOW_HEIGHT/2 - 200))
            elif 3 < elapsed_seconds < 4:
                go_message = self.font_timer.render('GO!!!', 1, GREEN)
                self.screen.blit(go_message,
                                 (WINDOW_WIDTH/2 - go_message.get_width()/2,
                                  WINDOW_HEIGHT/2 - 200))
            else:
                self.restart_game = False

        else:
            self.draw_middle_line()
            self.paddle_group.update()
            self.ball_sprite.update()
            self.draw_scene_delimitor()
            self.display_fps()
            self.draw_players_scores()
            self.check_ball_collision()

    def draw_middle_line(self):
        pygame.draw.line(self.screen,
                         BLUE,
                         [WINDOW_WIDTH_PER2, 0],
                         [WINDOW_WIDTH_PER2, WINDOW_HEIGHT],
                         2)

    def ball_collision(self):
        if (pygame.sprite.collide_mask(self.ball, self.opponent_paddle) or
                pygame.sprite.collide_mask(self.ball, self.player_paddle)):
            pygame.mixer.Sound.play(self.ball_hit_sound)

            collision_paddle = pygame.sprite.spritecollide(self.ball,
                                                           self.paddle_group,
                                                           False)[0].rect
            debug(f"right = {self.ball.rect.right},"
                  f"x = {self.ball.rect.x},"
                  f"pleft = {collision_paddle.left}")
            self.ball.bounce()

    def check_ball_collision(self):
        if pygame.sprite.spritecollide(self.ball, self.paddle_group, False):
            pygame.mixer.Sound.play(self.ball_hit_sound)

            # The paddle with witch the  collision happens
            collision_paddle = pygame.sprite.spritecollide(self.ball,
                                                           self.paddle_group,
                                                           False)[0].rect

            debug(f"right = {self.ball.rect.right},"
                  f"x = {self.ball.rect.x},"
                  f"pleft = {collision_paddle.left}")

            if (abs(self.ball.rect.right - collision_paddle.left) < 10 and
                    self.ball.velocity_x > 0):
                self.ball.velocity_x *= -1

            if (abs(self.ball.rect.left - collision_paddle.right) < 10 and
                    self.ball.velocity_x < 0):
                self.ball.velocity_x *= -1

            if (abs(self.ball.rect.top - collision_paddle.bottom) < 10 and
                    self.ball.velocity_y < 0):
                self.ball.rect.top = collision_paddle.bottom
                self.ball.velocity_y *= -1

            if (abs(self.ball.rect.bottom - collision_paddle.top) < 10 and
                    self.ball.velocity_y > 0):
                self.ball.rect.bottom = collision_paddle.top
                self.ball.velocity_y *= -1

    def draw_scene_delimitor(self):
        # Left border line
        pygame.draw.line(self.screen,
                         (0, 115, 251),
                         [3, 0],
                         [3, WINDOW_HEIGHT],
                         8)

        # Top border line
        pygame.draw.line(self.screen,
                         (0, 115, 251),
                         [0, 3],
                         [WINDOW_WIDTH, 3],
                         8)

        # Right border line
        pygame.draw.line(self.screen,
                         (0, 115, 251),
                         [WINDOW_WIDTH - 3, 0],
                         [WINDOW_WIDTH - 3, WINDOW_HEIGHT],
                         8)

        # Bottom border line
        pygame.draw.line(self.screen,
                         (0, 115, 251),
                         [0, WINDOW_HEIGHT - 4],
                         [WINDOW_WIDTH, WINDOW_HEIGHT - 4],
                         8)

    def display_fps(self):
        fps_value = self.font_normal.render(
            f"FPS: {int(self.clock.get_fps())}",
            1,
            PURPLE
        )
        self.screen.blit(fps_value, (WINDOW_WIDTH - 90, WINDOW_HEIGHT - 50))

    def move_player_up(self):
        self.player_paddle.moveUp(7)

    def move_player_down(self):
        self.player_paddle.moveDown(7)

    def draw_players_scores(self):
        # Opponent score
        opponent_score = self.font_big.render(self.opponent.get_name() + ' : '
                                              + str(self.opponent.get_score()),
                                              1,
                                              BLACK)
        self.screen.blit(opponent_score,
                         (WINDOW_WIDTH/4 - opponent_score.get_width()/2,
                          FONT_SIZE)
                         )

        # Player score
        player_score = self.font_big.render(self.player.get_name() + ' : '
                                            + str(self.player.get_score()),
                                            1,
                                            BLACK)

        self.screen.blit(
            player_score,
            (WINDOW_WIDTH/2 + WINDOW_WIDTH/4 - player_score.get_width() / 2,
             FONT_SIZE)
        )
