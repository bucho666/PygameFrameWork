# -*- coding: utf-8 -*-
import sys
import pygame
from pygame.locals import *
import configfile

class GameRunner(object):
    DEFAULT_FONT_SIZE = 16
    DEFALUT_FPS = 60
    ALLOW_EVENTS = [QUIT, KEYDOWN, KEYUP, 
                JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP]

    def __init__(self, application):
        self._screen = None
        self._timer = Timer(self.DEFALUT_FPS)
        self._controller = []
        self._keyboard = KeyBoard()
        self._application = application

    def initialize_system(self):
        pygame.init()
        self._setup_event_filter()
        return self

    def _setup_event_filter(self):
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(self.ALLOW_EVENTS)

    def initialize_screen(self, width, height, depth, screen_flag=0):
        screen = pygame.display.set_mode((width, height), screen_flag, depth)
        default_font = pygame.font.get_default_font()
        font = pygame.font.Font(default_font, self.DEFAULT_FONT_SIZE)
        self._screen = Screen(screen, font)
        return self

    def initialize_controller(self, joypad_number, keybind_filename):
        self._initialize_joysticks()
        config = configfile.ConfigFile(keybind_filename).load()
        key_binds = [self._load_keybind(config, num) for num in range(joypad_number)]
        self._controller = [Controller(key_bind) for key_bind in key_binds]
        return self

    def _load_keybind(self, config, pad_num):
        bind = dict()
        section = '%dP' % (pad_num+1)
        for (name, value) in config.items(section):
            bind[value] = name
        return bind

    def _initialize_joysticks(self):
        for js_no in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(js_no).init()

    def set_caption(self, new_caption):
        pygame.display.set_caption(new_caption)
        return self

    def set_fps(self, new_fps):
        self._timer.set_fps(new_fps)
        return self

    def set_font(self, name, size):
        self._screen.set_font(pygame.font.SysFont(name, size))
        return self

    def run(self):
        while True:
            self.process()
            self.wait()

    def wait(self):
        self._timer.tick()

    def process(self):
        self.poll_events()
        self.update()
        self.draw()

    def poll_events(self):
        for event in pygame.event.get():
            self.poll_event(event)

    def poll_event(self, event):
        if event.type is QUIT: sys.exit()
        if event.type in [JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP]:
            self._controller[event.joy].recive_event(event)
        elif event.type in [KEYDOWN, KEYUP]:
            self._keyboard.append(event)

    def update(self):
        self._application.update(self._keyboard, self._controller)
        self.reset_input()

    def reset_input(self):
        self._keyboard.reset()
        for controller in self._controller:
            controller.reset_event()

    def draw(self):
        self._application.draw(self._screen)
        self._screen.update()

class Timer(object):
    def __init__(self, fps):
        self._fps = fps
        self._clock = pygame.time.Clock()

    def tick(self):
        self._clock.tick(self._fps)

    def set_fps(self, new_fps):
        self._fps = new_fps

class Screen(object):
    def __init__(self, screen, font):
        self._screen = screen
        self._font = font

    def set_font(self, new_font):
        self._font = new_font

    def fill(self, color=(0,0,0)):
        self._screen.fill(color)

    def write(self, pos, string, color):
        surface = self._font.render(string, True, color)
        self.draw(pos, surface)

    def draw(self, pos, surface):
        self._screen.blit(surface, pos)

    def update(self):
        pygame.display.update()

class JoyPadEvent(object):
    def __init__(self):
        self._down_keys = []
        self._pressed_state = dict()

    def append(self, event):
        if event.type is JOYAXISMOTION:
            self._append_axis_event(event)
        if event.type in [JOYBUTTONDOWN, JOYBUTTONUP]:
            self._append_button_event(event)

    def _append_axis_event(self, event):
        axis_num, value = (event.axis, int(round(event.value, 0)))
        axis = 'AXIS:%d' % axis_num
        self._pressed_state[axis] = value
        if value == 0: return
        self._down_keys.append((axis, value))

    def _append_button_event(self, event):
        button = 'BUTTON:%d' % event.button
        if event.type is JOYBUTTONDOWN:
            self._pressed_state[button] = 1
            self._down_keys.append((button, 1))
        elif event.type is JOYBUTTONUP:
            self._pressed_state[button] = 0
    
    def down_keys(self):
        return list(self._down_keys)

    def pressed_keys(self):
        return [(which, value) for (which, value) in \
                self._pressed_state.items() if value != 0]

    def reset(self):
        self._down_keys = []

class Controller(object):
    def __init__(self, keybind):
        self._joypad_event = JoyPadEvent()
        self._keybind = keybind

    def recive_event(self, event):
        self._joypad_event.append(event)

    def reset_event(self):
        self._joypad_event.reset()

    def pressed_keys(self):
        return self._bind_keys(self._joypad_event.pressed_keys())

    def down_keys(self):
        return self._bind_keys(self._joypad_event.down_keys())

    def down_raw_keys(self):
        return self._joypad_event.down_keys()

    def pressed_raw_keys(self):
        return self._joypad_event.pressed_keys()

    def _bind_keys(self, keys):
        bind_keys = []
        for key in keys:
            str_key = str(key)
            if not self._keybind.has_key(str_key): continue
            bind_keys.append(self._keybind[str_key])
        return bind_keys

class KeyBoard(object):
    def __init__(self):
        self._down_keys = []
        self._pressed_keys = []

    def reset(self):
        self._down_keys = []

    def append(self, event):
        if event.type is KEYDOWN:
            self._pressed_keys.append(event.key)
            self._down_keys.append(event.key)
        elif event.type is KEYUP:
            self._pressed_keys.remove(event.key)

    def down_keys(self):
        return list(self._down_keys)

    def pressed_keys(self):
        return self._pressed_keys

if __name__ == '__main__':
    class HelloWorld(object):
        TEXT_COLOR = (192,192,0)
        def update(self, keyboard, controllers):
            pass

        def draw(self, screen):
            screen.fill()
            screen.write((0, 0), 'Hello World', self.TEXT_COLOR)

    GameRunner(HelloWorld())\
        .initialize_system()\
        .initialize_screen(640, 480, 16)\
        .initialize_controller(4, 'config.ini')\
        .set_fps(30)\
        .set_font('Courier New', 18)\
        .set_caption('Hello World')\
        .run()

