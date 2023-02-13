import pygame

BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)
SCREEN_WIDHT = 700
SCREEN_HEIGHT = 560


class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(LIGHT_GREY)
        self.image.set_colorkey(LIGHT_GREY)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def moveUp(self, speed):
        self.rect.y -= speed

        # Prevent the paddle from going off the screen (bottom)
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, speed):
        self.rect.y += speed

        # Prevent the paddle from going off the screen (top)
        if self.rect.y > 460:
            self.rect.y = 460
