import pygame.sprite
import assets
import conf
from layer import Layer
from objects.column import Column


class Plane(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PLAYER
        self.image = assets.get_sprite("plane")
        self.image = pygame.transform.scale(self.image, (64, 40))
        self.image_1 = assets.get_sprite("plane_1")
        self.image_1 = pygame.transform.scale(self.image_1, (64, 40))
        self.images = [self.image, self.image_1]
        self.image_non_rotate = pygame.transform.rotate(self.images[0], 45)
        self.image_rotate = pygame.transform.rotate(self.images[1], -45)
        self.rect = self.image.get_rect(topleft=(50, 300))
        self.direction = 1  # Коэфицент направления самолета, где 1 - вверх, -1 - вниз
        super().__init__(*groups)

    def update(self):
        self.rect.y -= self.direction * 5
        self.images.insert(0, self.images.pop())

    def handle_event(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            self.direction *= -1
            if self.direction == 1:
                self.image = self.image_non_rotate
            else:
                self.image = self.image_rotate

    def check_collision(self, sprites):
        self.mask = pygame.mask.from_surface(self.image)
        for sprite in sprites:
            if (type(sprite) is Column and sprite.mask.overlap(self.mask, (self.rect.x - sprite.rect.x,
                                                                           self.rect.y - sprite.rect.y))
                    or self.rect.bottom + 32 >= conf.SCREEN_HEIGHT):
                return True
            if self.rect.top <= 0:
                self.direction = -1
                self.image = self.image_rotate
        return False

    def get_coord(self):
        return self.rect.x, self.rect.y
