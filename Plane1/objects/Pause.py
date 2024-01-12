import pygame.sprite
import assets
import conf
from layer import Layer


class Pause(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.OBSTACLE
        self.image = assets.get_sprite('pause')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(conf.SCREEN_WIDTH - 60, 0))
        super().__init__(*groups)

    def check(self):
        self.pause_menu = assets.get_sprite('pause_menu')
        self.rect_p = self.image.get_rect(topleft=(conf.SCREEN_WIDTH / 2 - 150, conf.SCREEN_HEIGHT / 2 - 90))
        return self.pause_menu, self.rect_p
