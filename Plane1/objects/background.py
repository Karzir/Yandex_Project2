import pygame.sprite
import assets
import conf
from layer import Layer


class Background(pygame.sprite.Sprite):
    def __init__(self, index, *groups):
        self._layer = Layer.BACKGROUND
        self.image = assets.get_sprite("background")
        self.rect = self.image.get_rect(topleft=(conf.SCREEN_WIDTH * index, 0))

        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2
        if self.rect.right <= 0:
            self.rect.x = conf.SCREEN_WIDTH
