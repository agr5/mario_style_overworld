import pygame

from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y) -> None:
        super().__init__(size, x, y, r'graphics\enemy\run')
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))
        self.speed = randint(3,5)

    def move(self):
        self.rect.x += self.speed

    def revese_image(self):
        if self.speed >0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed*=-1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.revese_image()
        # return super().update(shift)