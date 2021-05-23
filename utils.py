import math
import numpy as np
import matplotlib.pyplot as plt
import random

from globals import SIMULATED_DATA_FILE_NAME, NODES_COUNT, ANCHOR_STANDART_DEVIATION
from vector import Vector

def collect_row(node, anchor):
    angle = node.get_angle(anchor)
    return (node.x, node.y, anchor.x, anchor.y, angle)

def make_plot_from_csv(file):
    data = np.loadtxt(file, delimiter='\t', skiprows=1)
    nodes_coords = data[:, 0:2]
    anchors_a_coords = data[:, 2:4][::NODES_COUNT]
    anchors_b_coords = data[:, 4:6][::NODES_COUNT]
    anchors_coords = [*anchors_a_coords, *anchors_b_coords]

    plt.clf()
    for anchor in anchors_coords:
        plt.plot(anchor[0], anchor[1], 'r o')
    for node in nodes_coords:
        plt.plot(node[0], node[1], 'b o')
        
    plt.show()


def get_beacon(anchor, node):
    # process negative beacon values
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


if __name__ == '__main__':
    with open(SIMULATED_DATA_FILE_NAME) as file:
        make_plot_from_csv(file)