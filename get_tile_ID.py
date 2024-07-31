import pygame as pg
import pygame.freetype as pgft
from settings import TILE_SIZE

pg.init()
screen = pg.display.set_mode((544, 256))
font = pgft.Font(None, 16)
image = pg.image.load('rpg/map/rpg_tileset.png')
image = pg.transform.scale(image, (544, 256))

num = 0
for y in range(0, 256, TILE_SIZE):
    for x in range(0, 544, TILE_SIZE):
        font.render_to(image, (x+10, y+10), str(num))
        num += 1
        

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False

    screen.blit(image, (0, 0))
    pg.display.flip()