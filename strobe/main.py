from terminal_display import Display
import shutil
from terminal_display import Frame  

def every_other_one(frame):
    for i in enumerate(range(0, frame.height)):  
        for j in range(0, frame.width):
            frame.set_cell(j, i[1], '█')

w,h = shutil.get_terminal_size()
empty_frame = Frame(w,h)
full_frame = Frame(w,h, fill_char='█')

display = Display()

is_frame_full = False

while True:
    if is_frame_full:
        display.replace_frame(empty_frame)
    else:
        display.replace_frame(full_frame)
    is_frame_full = not is_frame_full
    display.draw_frame()
