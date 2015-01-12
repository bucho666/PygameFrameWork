# -*- coding: utf-8 -*-

class Sprite(object):
    _screen = None

    @classmethod
    def set_screen(cls, screen):
        cls._screen = screen

    def __init__(self, surface, position):
        self._surface = surface
        self._position = position

    def render(self):
        self._screen.draw(self._position, self._surface)

    def set_position(self, new_position):
        self._position = new_position

    def move(self, direction):
        self._position += direction
