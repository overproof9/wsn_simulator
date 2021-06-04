### Test code samples

from globals import PL0, PL_EXP

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'X: {self.x}\tY: {self.y}'


class Vector:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.x = self.end.x - self.start.x
        self.y = self.end.y - self.start.y
        self.len = math.sqrt(self.x**2 + self.y**2)
    
    def __repr__(self):
        return f'Start: {self.start}\nEnd{self.end}'
    
# [+] Get beacon
def get_beacon(anchor, node):
    # if end is lower than start -> beacon = 360 - phi, else phi   
    vector = Vector(anchor, node)
    cos = vector.x / vector.len
    phi = math.degrees(math.acos(cos))
    if vector.start.y < vector.end.y:
        return phi 
    else:
        return 360 - phi

def get_angles(anchor1, anchor2, node):
    angle1 = get_beacon(anchor1, node) - get_beacon(anchor1, anchor2)
    angle2 = get_beacon(anchor2, node) - get_beacon(anchor2, anchor1)

    return (abs(angle1), abs(angle2))

def get_angles_b(a1, a2, b1, b2):
    angle1 = b1 - get_beacon(a1, a2)
    angle2 = b2 - get_beacon(a2, a1)
    return angle1, angle2


def get_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)



class Circle(Point):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r

    def __repr__(self):
        return super().__repr__() + f"\tRad: {self.r}"

def get_intersect_points(c1, c2):
    # returns array of intersection points 
    # if no intersect = 0 elements      if 1 interserct - 1 point       if 2 then 2 points
    result = []
    rp = Point(0, 0)
    d = math.sqrt(pow(abs(c1.x - c2.x), 2) + pow(abs(c1.y - c2.y), 2))
    if (d > c1.r + c2.r):
        return result

    dtr = (c1.r**2 - c2.r**2 + d**2) / (d*2)
    h = math.sqrt(c1.r**2 - dtr**2)

    rp.x = c1.x + dtr*(c2.x - c1.x) / d
    rp.y = c1.y + dtr*(c2.y - c1.y) / d

    fx = rp.x + h*(c2.y - c1.y) / d
    fy = rp.y - h*(c2.x - c1.x) / d

    result.append(Point(fx, fy))
    if dtr == c1.r:
        return result
    
    sx = rp.x - h*(c2.y - c1.y) / d
    sy = rp.y + h*(c2.x - c1.x) / d
    result.append(Point(sx, sy))
    return result



def get_ss(locator, node):
    # simulation
    d = get_distance(locator, node)
    print(d)
    return PL0 + (-10) * PL_EXP * math.log10(d)


def get_radius_from_ss(ss):
    #calculation
    return pow(10, (ss - PL0) / (-10*PL_EXP))




if __name__ == '__main__':
    # c1 = Circle(3, 4, 2)
    # c2 = Circle(5, 6, 2)
    # print(get_intersect_points(c1,c2))
    # print(c1)
    locator = Point(5, 6)
    node = Point(5, 3)

    ss = get_ss(locator, node)
    rad = get_radius_from_ss(ss)
    print(f"SS: {ss}\tRAD: {rad:2.5f}")
