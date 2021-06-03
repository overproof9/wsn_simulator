import random

from globals import AXIS_X_LIMIT, AXIS_Y_LIMIT
from utils import get_angles_from_nodes


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @classmethod
    def create_random(cls):
        x = random.randint(*AXIS_X_LIMIT)
        y = random.randint(*AXIS_Y_LIMIT)
        return cls(x, y)

    def __eq__(self, o):
        return self.x == o.x and self.y == o.y

    
    def sim_aoa(self, anchor_a, anchor_b):
        angles = get_angles_from_nodes(anchor_a, anchor_b, self)
        return (self.x, self.y, anchor_a.x, anchor_a.y, anchor_b.x, anchor_b.y, *angles)

    def __repr__(self):
        return f'X: {self.x}\tY: {self.y}'
