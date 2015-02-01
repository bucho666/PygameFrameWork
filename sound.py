# -*- coding: utf-8 -*-
import time
import pygame
from pygame.locals import *

class Sound(object):
    _cache = dict()
    
    @classmethod
    def play(cls, sound_file):
        if sound_file not in cls._cache: cls.load(sound_file)
        cls._cache[sound_file].play()

    @classmethod
    def play_bgm(cls, music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)

    @classmethod
    def load(cls, sound_file):
        sound = pygame.mixer.Sound(sound_file)
        sound.set_volume(1.0)
        cls._cache[sound_file] = sound

if __name__ == '__main__':
    import unittest

    class Test(unittest.TestCase):
        def setUp(self):
            pygame.init()

        def testPlay(self):
            Sound.play('join.ogg')
            time.sleep(0.5)
            Sound.play('touch.ogg')
            time.sleep(1)
            Sound.play('join.ogg')
            while pygame.mixer.get_busy():
                time.sleep(0.1)

    unittest.main()

