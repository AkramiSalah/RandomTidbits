class Frame:
    def __init__(self, width, height, fill_char = ' '):
        self.width= width
        self.height= height
        self.buffer= [[fill_char for _ in range(width)]for _ in range(height)]
    
    def set_cell(self, x, y, char = '█'):
        self.buffer[y][x] = char

    def clear(self, fill_char = ' '):
        for y in range(self.height):
            for x in range(self.width):
                self.buffer[y][x] = fill_char