import pygame as pg
from settings import *
import csv

class Map:
    WALL_ID = [1, 2, 3, 7, 8, 9, 10, 11,
            12, 13, 14, 15, 16, 18, 19, 20,
            24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35,
            36, 37, 41, 42, 43, 44, 45, 46,
            47, 48, 49, 50, 52, 53, 54, 58,
            59, 60, 61, 65, 66, 67, 69, 70,
            75, 76, 77, 78, 79, 81,
            82, 83, 84, 92, 93, 94, 95, 96, 97, 98, 99,
            100, 101, 107, 108, 109, 110, 111, 112, 113, 114,
            115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
            125, 130, 131, 132, 133, 134, 135]
    NPC_ID = [i for i in range(119, 126)]
    """Class for storing attributes for the game map."""
    def __init__(self, game, csv_path, image_path, tile_size, spacing=0):
        """Run functions to create a map."""
        self.data_list = self.parse_csv(csv_path)
        self.image_list = self.parse_images(image_path, tile_size, spacing)
        self.load_tiles(game)
        self.width = len(self.data_list[0]) * TILE_SIZE
        self.height = len(self.data_list) * TILE_SIZE
        
    def parse_images(self, image_path, tile_size, spacing):
        """Return a list of tile images from a given tileset."""
        image_list = []
        image = pg.image.load(image_path).convert()
        if tile_size != TILE_SIZE:
            scale = TILE_SIZE//tile_size
            spacing *= scale
            current_size = image.get_size()
            target_size = tuple(i * scale for i in current_size)
            image = pg.transform.scale(image, target_size)
        w, h = image.get_size()
        for y in range(0, h, TILE_SIZE+spacing):
            for x in range(0, w, TILE_SIZE+spacing):
                tile = image.subsurface(x, y, TILE_SIZE, TILE_SIZE)
                image_list.append(tile)
        return image_list
    
    def parse_csv(self, csv_path):
        """Return a list pf data from a given csv file."""
        with open(csv_path) as file:
            reader = csv.reader(file)
            data = list(reader)
            return data
        
    def load_tiles(self, game):
        """Create tile objects."""
        for y, row in enumerate(self.data_list):
            for x, index in enumerate(row):
                collidable = int(index) in Map.WALL_ID
                Tile(game, x, y, self.image_list[int(index)], collidable)

class Tile(pg.sprite.Sprite):
    """Class for storing atributes related to a single tile."""
    def __init__(self, game, x, y, image, is_wall=False):
        """Create a tile sprite in given the position."""
        self._layer = GROUND_LAYER
        if is_wall:
            groups = game.all_sprites, game.walls
        else:
            groups = game.all_sprites
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Camera:
    """Class created for moving the tiles depending on where the player moves."""
    def __init__(self, map_w, map_h):
        """Initialize the offset variable and recieve map size."""
        self.offset = (0, 0)
        self.map_w = map_w
        self.map_h = map_h

    def update(self, target):
        """Make the camera follow the target and limit the movement."""
        x = -target.rect.x + WIDTH//2
        y = -target.rect.y + HEIGHT//2
        x = min(0, x)
        y = min(0, y)
        x = max(x, -self.map_w+WIDTH)
        y = max(y, -self.map_h+HEIGHT)
        self.offset = (x, y)

    def apply(self, object):
        """Move the object by the offset variable."""
        return object.rect.move(self.offset)