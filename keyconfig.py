# -*- coding: utf-8 -*-
import configfile
from color import Color
import framework
from framework import Game

class KeyConfig(Game):
    def __init__(self, controller_num):
        Game.__init__(self)
        config = configfile.ConfigFile('config.ini').load()
        self._load_key_list(config)
        self._player_status = [PlayerState(num, config) for num in range(controller_num)]

    def _load_key_list(self, config):
        [(key, key_list)] = config.items('Keys')
        PlayerState.set_keys(key_list.split())

    def update(self):
        for status, controller in zip(self._player_status, self._controllers):
            status.update(controller)

    def draw(self):
        self._screen.fill()
        for player_state in self._player_status:
            player_state.draw(self._screen)

class PlayerState(object):
    keys = []
    def __init__(self, controller_num, config):
        self._controller_num = controller_num
        self._current_state = 0
        self._status = \
            [Ready(self, self._controller_num)] + \
            [KeyBinder(self, self._controller_num, key, config) for key in self.keys] + \
            [Done(self._controller_num)]

    @classmethod
    def set_keys(cls, key_list):
        cls.keys = key_list

    def update(self, controller):
        self._status[self._current_state].update(controller)

    def draw(self, screen):
        self._status[self._current_state].draw(screen)

    def next(self):
        if self._current_state + 1 >= len(self._status): return
        self._current_state += 1

class State(object):
    TEXT_COLOR = Color.SILVER
    def __init__(self, controller_num):
        self._controller_num = controller_num
     
    def write(self, screen, string):
        screen.write((0, self._controller_num * 40), 
                "[%dP] %s" % ((self._controller_num+1), string),
                self.TEXT_COLOR) 

class KeyBinder(State):
    def __init__(self, state, controller_num, target_key, config):
        State.__init__(self, controller_num)
        self._state = state
        self._target_key = target_key
        self._config = config
        
    def update(self, controller):
        keys = controller.down_raw_keys()
        if not keys: return
        key = str(keys[0])
        self._bind(key)
        self._state.next()

    def _bind(self, key):
        section = '%dP' % (self._controller_num+1)
        self._config.set(section, self._target_key, key)

    def draw(self, screen):
        self.write(screen, self._target_key)

class Ready(State):
    TEXT_COLOR = Color.YELLOW
    def __init__(self, state, controller_num):
        State.__init__(self, controller_num)
        self._state = state

    def update(self, controller):
        if controller.down_raw_keys():
            self._state.next()
    
    def draw(self, screen):
        self.write(screen, 'Push eny key')

class Done(State):
    TEXT_COLOR = Color.LIME
    def update(self, controller):
        pass
    
    def draw(self, screen):
        self.write(screen, 'Done')

if __name__ == '__main__':
    CONTROLLER_NUM = 4
    framework.GameRunner(KeyConfig(CONTROLLER_NUM))\
        .initialize_system()\
        .initialize_screen(640, 480, 16)\
        .initialize_controller(CONTROLLER_NUM, 'config.ini')\
        .set_fps(30)\
        .set_font('Courier New', 18)\
        .set_caption('KeyConfig')\
        .run()

