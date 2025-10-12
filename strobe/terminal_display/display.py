from .frame import Frame
from .renderer import Renderer 
import shutil

class Display:
    def __init__(self):
        self.renderer = Renderer()
        w, h = shutil.get_terminal_size()
        self.frame = Frame(w, h)
    
    def edit_frame(self, func):
        func(self.frame)
    
    def draw_frame(self):
        self.renderer.render_frame(self.frame)
    
    def clear_frame(self):
        self.frame.clear()

    def replace_frame(self, new_frame):
        self.frame = new_frame