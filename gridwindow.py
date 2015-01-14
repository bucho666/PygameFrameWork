# -*- coding: utf-8 -*-
import sys
import framework
from color import Color
from coordinate import Coordinate
from coordinate import Direction

class GridWindow(object):
    def __init__(self, screen, position, grid_size):
        self._position = position
        self._grid_size = grid_size
        self._screen = screen

    def write(self, pos, string, color):
        self._screen.write(self._convert_pos(pos), string, color)

    def draw(self, pos, surface):
        self._screen.draw(self._convert_pos(pos), surface)

    def _convert_pos(self, pos):
        return (self._position + pos * self._grid_size).xy()

if __name__ == '__main__':
    class GridWindowDemo(framework.Game):
        POSITION = Coordinate(0, 0)
        GRID_SIZE = Coordinate(10, 18)
        def __init__(self):
            framework.Game.__init__(self)
            self._window = None
            self._character_pos = Coordinate(1, 1)

        def update(self):
            down_keys =  self._keyboard.down_keys()
            if not down_keys: return
            key = down_keys[0]
            if key == ord('h'): self._move(Direction.LEFT)
            if key == ord('j'): self._move(Direction.DOWN)
            if key == ord('k'): self._move(Direction.UP)
            if key == ord('l'): self._move(Direction.RIGHT)
            if key == ord('q'): sys.exit()

        def _move(self, direction):
            self._character_pos += direction

        def set_screen(self, screen):
            self._screen = screen
            self._window = GridWindow(screen, self.POSITION, self.GRID_SIZE)

        def render(self):
            self._screen.fill()
            self._window.write(self._character_pos, '@', Color.LIME)

    framework.GameRunner(GridWindowDemo())\
        .initialize_system()\
        .initialize_screen(640, 480, 16)\
        .set_fps(30)\
        .set_font('Courier New', 18)\
        .set_caption('GridWindowDemo')\
        .run()
