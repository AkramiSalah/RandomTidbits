class Frame:
    def __init__(self, width, height, fill_char = ' '):
        self.width= width
        self.height= height
        self.buffer= [[fill_char for _ in range(width)]for _ in range(height)]
    
    def frame_width(self):
        return self.width
    
    def frame_height(self):
        return self.height

    def set_cell(self, x, y, char = '█'):
        self.buffer[y][x] = char

    def clear(self, fill_char = ' '):
        for y in range(self.height):
            for x in range(self.width):
                self.buffer[y][x] = fill_char

    def set_point(self, point, char = '█'):
        self.buffer[point.y][point.x] = char