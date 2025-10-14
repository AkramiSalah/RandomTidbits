from terminal_display import Display
import shutil
from terminal_display import Frame  
import msvcrt, sys
import time

from snake import Snake, DIRECTIONS
from fruit import Fruit

display = Display()
current_frame = Frame(*shutil.get_terminal_size())


# Create snake and fruit instances
snake = Snake()
fruit = Fruit()

while True:
    current_frame.clear()
    next_head = snake.get_head() + snake.direction
    if next_head == fruit.get_position():
        snake.eat()
        fruit.random_respawn(current_frame)

    snake.move_snake()
    if snake.hits_itself() or snake.hits_wall(current_frame):
        print("Game Over!")
        sys.exit()
    
    fruit.frame_fruit(current_frame)
    snake.frame_snake(current_frame)
    
    display.replace_frame(current_frame)
    display.draw_frame()

    if msvcrt.kbhit():        # True if a key has been pressed
        key = msvcrt.getch()
        if key == b'\x1b':     # ESC
            sys.exit()
        elif key == b'H':       # up arrow
            snake.change_direction(DIRECTIONS['U'])
        elif key == b'P':       # down arrow
            snake.change_direction(DIRECTIONS['D'])
        elif key == b'K':       # left arrow
            snake.change_direction(DIRECTIONS['L'])
        elif key == b'M':       # right arrow
            snake.change_direction(DIRECTIONS['R'])
    
    time.sleep(0.1333333333333333)  # ~7.5 FPS