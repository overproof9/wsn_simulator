import numpy as np
import math
import matplotlib.pyplot as plt

from anchor import AnchorNode
from globals import TRIANGULATION_SIMULATED_DATA, AXIS_X_LIMIT, AXIS_Y_LIMIT
from utils import get_angles_from_beacons


def get_distance(anchor_a, anchor_b):
    delta_x = anchor_b.x - anchor_a.x
    delta_y = anchor_b.y - anchor_a.y
    return math.sqrt(delta_x**2 + delta_y**2)


def found_node(anchor_a, anchor_b, beacon_a, beacon_b):
    distance = get_distance(anchor_a, anchor_b)
    phi_c = math.radians(beacon_a - beacon_b)
    phi_a, phi_b = get_angles_from_beacons(anchor_a, anchor_b, beacon_a, beacon_b)
    phi_a = math.radians(phi_a)
    phi_b = math.radians(beacon_b)

    r = abs((distance * math.sin(phi_a)) / math.sin(phi_c))

    delta_x = r * math.cos(phi_b)
    delta_y = r * math.sin(phi_b)

    x = min(anchor_b.x + delta_x, AXIS_X_LIMIT[1])
    y = min(anchor_b.y + delta_y, AXIS_Y_LIMIT[1])

    if x < 0 or y < 0:
        return (0, 0)                       # if coords < 0 smth went wrong put to 0,0
    return(round(x, 2), round(y, 2))
    

def find_all_nodes(file):
    nodes = []
    data = np.loadtxt(file, delimiter='\t', skiprows=1)

    for row in data:
        anchor_a = AnchorNode(row[2], row[3])
        anchor_b = AnchorNode(row[4], row[5])
        beacon_a = row[8]
        beacon_b = row[9]
        beacon_noise_a = row[10]
        beacon_noise_b = row[11]
        real_calculated = found_node(anchor_a, anchor_b, beacon_a, beacon_b)
        noise_calculated = found_node(anchor_a, anchor_b, beacon_noise_a, beacon_noise_b)

        nodes.append((row[0], row[1], *real_calculated, *noise_calculated))

    return nodes


if __name__ == '__main__':
    """
    Localize nodes using only angles and anchors coords
    Use all combinations of anchors pairs ang get average coords to better precise
    """



    nodes = find_all_nodes(TRIANGULATION_SIMULATED_DATA)

    for node in nodes:
        plt.plot(node[0], node[1], 'b o')       # real data
        plt.plot(node[2], node[3], 'r x')       # triangulation exact beacons ensure calculations are correct
        plt.plot(node[4], node[5], 'g x')       # triangulation noise beacons
        if (node[4] > 0 and node[5] > 0):                   
            plt.plot([node[4], node[0]], [node[5], node[1]])    # drow relation lines only when node is correct
    
    plt.show()
