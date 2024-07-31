import pygame as pg
import pygame.freetype as pgft
from settings import *
       

class Npc(pg.sprite.Sprite):
    """Class for creating NPCs."""
    def __init__(self, game, image, pos, text, liste, text_speed):
        """Initialize npc variables."""
        self._layer = GROUND_LAYER
        groups = game.all_sprites, game.walls
        super().__init__(groups)
        self.image = image
        self.text = text
        self.game = game
        self.rect = self.image.get_rect(center=pos)
        self.message = Message(game, self.text, (pos[0]-40, pos[1]-40), None, liste)
        self.stop = False
        self.change_exists = False
        self.text_speed = text_speed

    def talk(self):
        """Make an npc talk."""
        if self.rect.colliderect(self.game.player.rect):
            self.message.print()
        elif self.message.groups():
            self.message.clear()

    def update(self):
        """Update the class."""
        self.talk()
    
class Message(pg.sprite.Sprite):
    """Class for storing message atributes."""
    def __init__(self, game, text, pos, font, listt):
        self._layer = TEXT_LAYER
        super().__init__(game.all_sprites)
        self.game = game
        self.list = listt
        self.text = self.list[0]
        self.text_pos = (10, 10)
        self.current_symbol = 0
        self.displayed_text = ''
        self.font = pgft.Font(font, 16)
        surf, text_rect = self.font.render(self.text)
        self.image = pg.Surface((text_rect.w+30, text_rect.h+17.5), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.border = pg.Rect((0, 0), self.rect.size)
        self.border.w = text_rect.w+20
        self.pos = pos
        self.text_index = 0

    def print(self):
        """Print the message on the screen."""
        self.text = self.list[self.text_index%len(self.list)]
        self.current_symbol += 0.5
        self.displayed_text = self.text[:int(self.current_symbol)]
        self.add(self.game.all_sprites)
        text_surf, text_rect = self.font.render(self.displayed_text)
        self.image.fill((0, 0, 0, 0))
        self.image.blit(text_surf, self.text_pos)
        pg.draw.rect(self.image, (0, 0, 255), self.border, width=5, border_radius=10)

    def clear(self):
        """Remove the message."""
        self.current_symbol = 0
        self.displayed_text = ''
        self.kill()
    
    def change_text(self, new_text):
        """Change the text."""
        self.clear()
        self.text = new_text
        surf, text_rect = self.font.render(self.text)
        self.image = pg.Surface((text_rect.w+30, text_rect.h+17.5), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        self.border = pg.Rect((0, 0), self.rect.size)
        self.border.w = text_rect.w+20