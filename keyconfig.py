# -*- coding: utf-8 -*-
import configfile

class KeyConfig(object):
    def __init__(self, controller_num):
        self._player_status = [PlayerState(num) for num in range(controller_num)]

    def update(self, keyboard, controllers):
        for status, controller in zip(self._player_status, controllers):
            status.update(controller)

    def draw(self, screen):
        screen.fill()
        for player_state in self._player_status:
            player_state.draw(screen)

class PlayerState(object):
    KEYS = [ 'UP', 'DOWN', 'LEFT', 'RIGHT', 'HOLD' ]
    def __init__(self, controller_num):
        self._controller_num = controller_num
        self._current = 0
        config = configfile.ConfigFile('config.ini')
        self._status = \
            [Ready(self, controller_num)] +\
            [KeyBinder(self, controller_num, key, config) for key in self.KEYS] +\
            [Done(controller_num)]

    def update(self, controller):
        self._status[self._current].update(controller)

    def draw(self, screen):
        self._status[self._current].draw(screen)

    def next(self):
        if self._current + 1 >= len(self._status): return
        self._current += 1

class State(object):
    TEXT_COLOR = (192,192,192)
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
    TEXT_COLOR = (255,255,0)
    def __init__(self, state, controller_num):
        State.__init__(self, controller_num)
        self._state = state

    def update(self, controller):
        if controller.down_raw_keys():
            self._state.next()
    
    def draw(self, screen):
        self.write(screen, 'Push eny key')

class Done(State):
    TEXT_COLOR = (0,255,0)
    def update(self, controller):
        pass
    
    def draw(self, screen):
        self.write(screen, 'Done')

if __name__ == '__main__':
    import framework
    CONTROLLER_NUM = 4
    framework.GameRunner(KeyConfig(CONTROLLER_NUM))\
        .initialize_system()\
        .initialize_screen(640, 480, 16)\
        .initialize_controller(CONTROLLER_NUM, 'config.ini')\
        .set_fps(30)\
        .set_font('Courier New', 18)\
        .set_caption('KeyConfig')\
        .run()

