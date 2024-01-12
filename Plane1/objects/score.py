import pygame.sprite
import assets
import conf
from layer import Layer


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.value = 0
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)

        self.__create()

        super().__init__(*groups)

    def __create(self):
        self.str_value = str(self.value)

        self.images = []
        self.width = 0

        for str_value_char in self.str_value:
            img = assets.get_sprite(str_value_char)
            self.images.append(img)
            self.width += img.get_width()

        self.height = self.images[0].get_height()
        self.image = pygame.surface.Surface((self.width+20, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(conf.SCREEN_WIDTH / 2, 50))

        for n, img in enumerate(self.images):
            self.image.blit(img, (n * img.get_width(), 0))

    def update(self):
        self.__create()
