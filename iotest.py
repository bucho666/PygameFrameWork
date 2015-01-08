# -*- coding: utf-8 -*-
class IOTest(object):
    def __init__(self):
        self._messages = []

    def write(self, message):
        self._messages.append(message)

    def update(self, keyboard, joypads):
        self.write('[KEY BOARD]')
        self.write_keyboard_state(keyboard)
        self.write('')
        self.write('[JOY PAD]')
        self.write_joypads_state(joypads)

    def write_keyboard_state(self, keyboard):
        self.write('pressed keys: %s' % str(keyboard.pressed_keys()))
        self.write('down keys: %s' % str(keyboard.down_keys()))

    def write_joypads_state(self, joypads):
        for joypad_id, joypad in enumerate(joypads):
            self.write_joypad_state(joypad_id, joypad)

    def write_joypad_state(self, joypad_id, joypad):
        player_id = joypad_id + 1
        self.write('[%dP] pressed keys: %s' % \
                (player_id, str(joypad.pressed_keys())))
        self.write('[%dP] down keys: %s' % \
                (player_id, str(joypad.down_keys())))

    def draw(self, screen):
        screen.fill()
        for line, message in enumerate(self._messages):
            screen.write((0, line*18), message, (192,192,192))
        self._messages = []

if __name__ == '__main__':
    import framework
    framework.GameRunner(IOTest())\
        .initialize_system()\
        .initialize_screen(640, 480, 16)\
        .initialize_controller(4, 'config.ini')\
        .set_fps(30)\
        .set_font('Courier New', 18)\
        .set_caption('IO Test')\
        .run()

