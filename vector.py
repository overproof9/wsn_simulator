import math

class Vector:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.x = self.end.x - self.start.x
        self.y = self.end.y - self.start.y
        self.len = math.sqrt(self.x**2 + self.y**2)
    
    def __repr__(self):
        return f'Start: {self.start}\nEnd{self.end}'
