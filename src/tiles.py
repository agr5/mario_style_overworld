import pygame
from settings import tile_size
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self,size, x, y) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface) -> None:
        super().__init__(size, x, y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, x, y) -> None:
        surface = pygame.image.load(r'graphics\terrain\crate.png').convert_alpha()
        super().__init__(size, x, y, surface)
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path) -> None:
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
    def animate(self):
        self.frame_index += 0.15 # subjective
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        return super().update(shift)
    

class Coin(AnimatedTile):
    def __init__(self, size, x, y, path) -> None:
        super().__init__(size, x, y, path)
        center_x = x + size//2
        center_y = y + size//2
        self.rect = self.image.get_rect(center=(center_x, center_y))

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset) -> None:
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect = self.image.get_rect(center=(x, offset_y))