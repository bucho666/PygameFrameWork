# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from color import Color

class TileSheet(object):
    def __init__(self, surface, size):
        self._size = size
        self._surface = surface

    def get_tile(self, (x, y)):
        w, h = self._size
        return self._surface.subsurface(Rect((x*w, y*h), self._size))

class AsciiTileSheet(object):
    def __init__(self):
        self._surface = dict()

    def initialize(self, fontname, size):
        font = pygame.font.SysFont(fontname, size)
        characters = ''.join([chr(n) for n in range(32, 127)])
        tilesheet = self.create_tilesheet(font, characters)
        for y, color in enumerate(Color.LIST):
           for x, ch in enumerate(characters):
                self._surface[(ch, color)] = tilesheet.get_tile((x, y))
        return self

    def create_tilesheet(self, font, characters):
        w, h = self.get_size(font)
        src_w, src_h = len(characters) * w, len(Color.LIST) * h
        source_sheet = pygame.Surface((src_w, src_h))
        for line, color in enumerate(Color.LIST):
            line_surface = font.render(characters, True, color)
            source_sheet.blit(line_surface, (0, line * h))
        return TileSheet(source_sheet, (w, h))

    def get_tile(self, char, color):
        return self._surface[(char, color)]

    def get_size(self, font):
        return font.render(' ', True, (0,0,0)).get_size()
        
if __name__ == '__main__':
    import random
    from framework import Game
    class AsciiTileSheetDemo(Game):
        def __init__(self):
            Game.__init__(self)
            self._tile = AsciiTileSheet()

        def initialize(self):
            self._tile.initialize('Courier New', 18)

        def render(self):
            self._screen.fill()
            chars = [chr(n) for n in range(32, 127)]
            for y in range(24):
                for x in range(53):
                    self._screen.draw((x*12, y*20), 
                            self._tile.get_tile(random.choice(chars),
                                random.choice(Color.LIST)))

    from framework import GameRunner
    demo = AsciiTileSheetDemo()
    runner = GameRunner(demo)\
        .initialize_system()\
        .initialize_screen(640, 480, 16)\
        .set_fps(24)\
        .set_caption('Ascii Tile Demo')
    runner.run()
