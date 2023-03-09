from csv import reader
from settings import tile_size
import pygame
from os import walk
import os


def import_folder(path) -> list:
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = os.path.join(path,image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(row)

    return terrain_map

def import_cut_graphics(path)->list:
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = surface.get_width()//tile_size
    tile_num_y = surface.get_height()//tile_size

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            # pygame.SRCALPHA # set all pixels not being used to invisble
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

