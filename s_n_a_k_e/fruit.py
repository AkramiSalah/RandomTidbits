from terminal_display import Point

class Fruit:
    def __init__(self, position = Point(10,10)):
        self.position = position

    def get_position(self):
        return self.position    
    
    def frame_fruit(self, frame):
        frame.set_point(self.position, char='*')
    
    def random_respawn(self, frame):
        import random
        new_x = random.randint(0, frame.frame_width() - 1)
        new_y = random.randint(0, frame.frame_height() - 1)
        self.position = Point(new_x, new_y)