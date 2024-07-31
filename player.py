import pygame as pg
from core import SpriteSheet
from pygame.math import Vector2
from settings import *
import math


"""File for player class."""
class Player(pg.sprite.Sprite):
    """Class for storing attributes related to the player."""
    speed = 6
    def __init__(self, game, spritesheet_path, pos):
        """Initialize required variables."""
        self._layer = PLAYER_LAYER
        super().__init__(game.all_sprites)
        self.spritesheet = SpriteSheet(spritesheet_path, 2)
        self.load_images()
        self.image = self.walk_right[0]
        self.rect = self.image.get_rect(center=pos)
        self.velocity = Vector2(0, 0)
        self.frame = 0
        self.animation_length = 4
        self.last_update = 0
        self.game = game
        self.hitbox = pg.Rect(self.rect.x, self.rect.y, self.rect.w/2, self.rect.h/4)
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom - 5

    def move(self):
        """Moving player with vectors."""
        self.velocity.update(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.velocity.y = -1
        if keys[pg.K_a]:
            self.velocity.x = -1
        if keys[pg.K_s]:
            self.velocity.y = 1
        if keys[pg.K_d]:
            self.velocity.x = 1
        if self.velocity.length() > 1:
            self.velocity.x = 0
        self.velocity *= math.ceil(Player.speed*self.game.dt)
        if not self.will_collide():
            speed = 4.2
            self.rect.center += self.velocity * speed
            self.hitbox.center += self.velocity * speed

    def update(self):
        """Move and animate player."""
        self.move() 
        self.animate()

    def load_images(self):
        """Load images from the spritesheet into separated lists."""
        self.walk_right = []
        self.walk_left = []
        self.walk_down = []
        self.walk_up = []
        w, h = self.spritesheet.width//4, self.spritesheet.height//4
        for i in range(0, w*4, w):
            self.walk_down.append(self.spritesheet.get_image(i, 0, w, h))
            self.walk_left.append(self.spritesheet.get_image(i, h, w, h))
            self.walk_right.append(self.spritesheet.get_image(i, h*2, w, h))
            self.walk_up.append(self.spritesheet.get_image(i, h*3, w, h))

    def animate(self, frame_length=100):
        """Animate the player if moving."""
        if self.velocity.length() > 0:
            if self.velocity.y > 0:
                self.animation_cycle = self.walk_down
            elif self.velocity.y < 0:
                self.animation_cycle = self.walk_up
            elif self.velocity.x > 0:
                self.animation_cycle = self.walk_right
            elif self.velocity.x < 0:
                self.animation_cycle = self.walk_left
            self.frame = (self.frame + self.game.dt * Player.speed) % self.animation_length
            self.image = self.animation_cycle[int(self.frame)]

    def will_collide(self):
        """Check if the player will collide with an object."""
        target_rect = self.hitbox.move(self.velocity)
        for tile in self.game.walls:
            if target_rect.colliderect(tile.rect):
                return True
        return False