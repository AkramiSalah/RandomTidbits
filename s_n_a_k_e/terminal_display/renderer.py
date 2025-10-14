import os
import shutil

class Renderer:
    def __init__(self):
        self.last_frame = None
        self.width, self.height = shutil.get_terminal_size()

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render_frame(self, frame):
        for y in range(frame.height):
            for x in range(frame.width):
                print(frame.buffer[y][x], end='')
            print()
        self.last_frame = frame