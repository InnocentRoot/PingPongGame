import pygame
from settings import (LIGHT_GREY, WINDOW_HEIGHT)


class Opponent(pygame.sprite.Sprite):

    def __init__(self, color, width, height, game):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(LIGHT_GREY)
        self.image.set_colorkey(LIGHT_GREY)
        self.game = game

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        # if game.config.get_difficulty() == 1:
        #     self.velocity = 7
        # else:
        #     self.velocity = 5
        self.velocity = 7 * game.config.get_difficulty()

        self.score = 0

    def get_score(self):
        return self.score

    def increment_score(self):
        self.score += 1
        return self.score

    def update(self):
        # Dont't go off the screen
        if self.rect.y <= 0:
            self.rect.y = 0

        if self.rect.y >= WINDOW_HEIGHT - 100:
            self.rect.y = WINDOW_HEIGHT - 100

    def moveUp(self):
        self.rect.y -= self.velocity

    def moveDown(self):
        self.rect.y += self.velocity
