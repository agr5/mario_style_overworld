import pygame

from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height
from tiles import Tile, StaticTile, Crate, AnimatedTile, Coin, Palm
from decoration import Sky, Water, Cloud
from enemy import Enemy

class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = +6

        # player setup
        player_layout = import_csv_layout(level_data.get('player'))
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_data.get('terrain'))
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data.get('grass'))
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crate_layout = import_csv_layout(level_data.get('crates'))
        self.crates_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data.get('coins'))
        self.coins_sprites = self.create_tile_group(coin_layout, 'coins')

        # foreground palmtrees
        fg_palms_layout = import_csv_layout(level_data.get('fg_palms'))
        self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # background palms
        bg_palms_layout = import_csv_layout(level_data.get('bg_palms'))
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # enemy
        enemy_layout = import_csv_layout(level_data.get('enemies'))
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data.get('constraints'))
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0])*tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Cloud(400, level_width, 25)
        
        pass
    
    
    def create_tile_group(self, layout, type) -> pygame.sprite.Group:
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(r'graphics\terrain\terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    elif type == 'grass':
                        grass_tile_list = import_cut_graphics(r'graphics\decoration\grass\grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    
                    elif type == 'crates':
                        sprite = Crate(tile_size, x, y)
                    
                    elif type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, r'graphics\coins\gold')
                        elif val == '1':
                            sprite = Coin(tile_size, x, y, r'graphics\coins\silver')

                    elif type == 'fg_palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y, r'graphics\terrain\palm_small', 38)
                        if val == '1':
                            sprite = Palm(tile_size, x, y, r'graphics\terrain\palm_large', 64)
                        if val == '2':
                            sprite = Palm(tile_size, x, y, r'graphics\terrain\palm_bg', 64)
                    
                    elif type == 'bg_palms':
                        sprite = Palm(tile_size, x, y, r'graphics\terrain\palm_bg', 64)

                    elif type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    elif type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    
                    sprite_group.add(sprite) # Risky if all 'ifs' fail...

        return sprite_group
    
    
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    # player
                    print('Player goes here')
                if val == '1':
                    hat_surface = pygame.image.load(r'graphics\character\hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)
    

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()


    def run(self):
        # run entire game/level

        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # bg_palms
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        # crate
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # fg_palms
        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)
        

        
        pass