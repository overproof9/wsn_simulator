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

def get_beacon_neg(anchor, node):
# if end is lower than start -> beacon = -phi, else phi   
    vector = Vector(anchor, node)
    cos = vector.x / vector.len
    phi = math.degrees(math.acos(cos))
    if vector.start.y > vector.end.y:
        return -phi 
    else:
        return phi

def get_angles(anchor1, anchor2, node):
    angle1 = get_beacon(anchor1, node) - get_beacon(anchor1, anchor2)
    angle2 = get_beacon(anchor2, node) - get_beacon(anchor2, anchor1)

    return (abs(angle1), abs(angle2))

def get_angles_b(a1, a2, b1, b2):
    angle1 = b1 - get_beacon(a1, a2)
    angle2 = b2 - get_beacon(a2, a1)
    return angle1, angle2

if __name__ == '__main__':
    anchor1 = Point(51, 80)
    anchor2 = Point(69, 35)

    node1 = Point(4,56)

    b1 = get_beacon(anchor1, node1)
    b2 = get_beacon(anchor2, node1)

    print(get_angles_b(anchor1, anchor2, b1, b2))

    # print(get_angles_b(anchor1, anchor2, node1))