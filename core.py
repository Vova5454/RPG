import pygame as pg

"""The class of a spritesheet."""
class SpriteSheet():
    """Class for storing and managing spritesheets."""
    def __init__(self, file_path, scale=1):
        """Preparing file for cutting and scaling."""
        sheet = pg.image.load(file_path).convert_alpha()
        width, height = sheet.get_size()
        target_size = (int(width * scale), int(height * scale))
        self.sheet = pg.transform.scale(sheet, target_size)
        self.width, self.height = self.sheet.get_size()

    def get_image(self, x, y, width, height):
        """Cut and return a piece of spritesheet."""
        return self.sheet.subsurface(x, y, width, height)