import math
# from proj.pg import get_beacon
import random

from matplotlib.pyplot import cla
from numpy.lib.ufunclike import _dispatcher

from globals import ANCHOR_STANDART_DEVIATION, NODES_COUNT, AOA_MIN, AOA_MAX, AXIS_X_LIMIT, AXIS_Y_LIMIT
from vector import Vector

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

    
    def get_simulated_data(self, anchor_a, anchor_b):
        angles = get_angles_from_nodes(anchor_a, anchor_b, self)
        return (self.x, self.y, anchor_a.x, anchor_a.y, anchor_b.x, anchor_b.y, *angles)

    # def get_angle(self, node):
    #     delta_x = self.x - node.x
    #     delta_y = self.y - node.y
    #     angle = math.atan(delta_y / delta_x)
    #     return math.degrees(angle)

    def __repr__(self):
        return f'X: {self.x}\tY: {self.y}'



def get_beacon(anchor, node):
    # if end is lower than start -> beacon = 360 - phi, else phi   
    vector = Vector(anchor, node)
    cos = vector.x / vector.len
    phi = math.degrees(math.acos(cos))
    if vector.start.y < vector.end.y:
        return phi 
    else:
        return 360 - phi


def get_angles_from_nodes(anchor_a, anchor_b, node):
    beacon_a = get_beacon(anchor_a, node) + random.randint(0, ANCHOR_STANDART_DEVIATION)        # noise
    beacon_b = get_beacon(anchor_b, node) + random.randint(0, ANCHOR_STANDART_DEVIATION)        # noise
    angle1 = get_beacon(anchor_a, node) - get_beacon(anchor_a, anchor_b)
    angle2 = get_beacon(anchor_b, node) - get_beacon(anchor_b, anchor_a)
    

    return (abs(angle1), abs(angle2), beacon_a, beacon_b)

def get_angles_from_beacons(anchor_a, anchor_b, beacon_a, beacon_b):
    angle_a = beacon_a - get_beacon(anchor_a, anchor_b)
    angle_b = beacon_b - get_beacon(anchor_b, anchor_a)
    return (abs(angle_a), abs(angle_b))
