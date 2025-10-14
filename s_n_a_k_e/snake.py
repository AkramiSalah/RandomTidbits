from collections import deque
from terminal_display import Point

DIRECTIONS = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
}

class Snake:
    def __init__(self, tail = Point(5,5), head = Point(6,5), direction = DIRECTIONS['R'], just_ate = False):
        self.body = deque()
        self.body.append(tail)
        self.body.append(head)
        self.direction = direction
        self.just_ate = just_ate
    
    def move_snake(self):  
        if not self.just_ate:   
            self.body.popleft()
            self.body.append(self.body[-1] + self.direction)
        else:
            self.body.append(self.body[-1] + self.direction)
            self.just_ate = False
    
    def change_direction(self, new_direction):
        self.direction = new_direction

    def eat(self):
        self.just_ate = True
    
    def get_body(self):
        return self.body    
    
    def get_head(self):
        return self.body[-1]
    
    def get_tail(self):
        return self.body[0]
    
    def hits_itself(self):
        head = self.get_head()
        return any(head == part for part in list(self.body)[:-1])
    
    def hits_wall(self, frame):
        head = self.get_head()
        return head.x < 0 or head.x >= frame.frame_width() or head.y < 0 or head.y >= frame.frame_height()
    
    def frame_snake(self, frame):
        for part in self.body:
            frame.set_point(part)

    
