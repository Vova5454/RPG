import pygame as pg
from settings import *
from player import Player
from map import Map, Camera
from npc import Npc
from core import SpriteSheet

class Game():
    """Generic class for holding the game atributes."""
    def __init__(self):
        """Create the game window."""
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.run = True

    def create_objects(self):
        """Initialize all sprites."""
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = Player(self, 'rpg/sprites/player_sheet.png', (WIDTH//1.5, HEIGHT//2))
        self.walls = pg.sprite.Group()
        self.map = Map(self, 'rpg/map/map.csv', 'rpg/map/rpg_tileset.png', 16)
        self.camera = Camera(self.map.width, self.map.height)
        self.text = "Why are you touching me?"
        self.one = Npc(self, self.map.image_list[125], (WIDTH//1.5, HEIGHT//1.5), self.text, [self.text, "Don't touch me.", "I'm angry >:(", 'STOP TOUCHING ME!', 'Dude stop.', 'You still here?', 'How many times do I have to tell you?', 'STOP', 'TOUCHING', 'ME!'], 800)
        self.two = Npc(self, self.map.image_list[0], (WIDTH//1.02, HEIGHT//1.3), '', ["BOO! I'm a talking grass.", 'Ok you can go now.'], 1250)
        self.three = Npc(self, self.map.image_list[16], (WIDTH//0.75, HEIGHT//2.1,), '', ['*A tree*', 'Meow', 'I am spikey.'], 1000)
        self.npcs = [self.one, self.two, self.three]
        self.stop = False
        self.change_exists = False

    def update(self):
        """Update all sprites."""
        self.all_sprites.update()
        self.camera.update(self.player)
        now = pg.time.get_ticks()
        for npc in self.npcs:
            if npc.message.displayed_text == npc.message.text:
                if not npc.stop:
                    npc.change = pg.time.get_ticks()
                    npc.change_exists = True
                npc.stop = True
            if npc.change_exists:
                if now - npc.change >= npc.text_speed:
                    npc.message.current_symbol = 0
                    npc.message.text_index += 1
                    npc.message.change_text(npc.message.list[npc.message.text_index%len(npc.message.list)])
                    npc.stop = False
                    npc.change_exists = False


    def draw(self):
        """Draw all sprites and objects and move sprites."""
        pg.display.set_caption(f'RPG FPS:{round(self.clock.get_fps(), 1)}')
        self.screen.fill(BG_COLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def get_events(self):
        """Check for input events."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.run = False
    
    def game_cycle(self):
        """The game loop."""
        while self.run:
            self.dt = self.clock.tick(60)/1000
            self.get_events()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = Game()
    game.create_objects()
    game.game_cycle()