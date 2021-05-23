import numpy as np
import math
import matplotlib.pyplot as plt

from functools import reduce

from anchor import AnchorNode
from globals import NODES_COUNT, SIMULATED_DATA_FILE_NAME, ANCHORS_COUNT
from node import Node, get_angles_from_beacons


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

    x = anchor_b.x + delta_x
    y = anchor_b.y + delta_y
    return(round(x, 2), round(y, 2))
    

def find_all_nodes(file):
    nodes = []
    data = np.loadtxt(file, delimiter='\t', skiprows=1)

    for row in data:
        anchor_a = AnchorNode(row[2], row[3])
        anchor_b = AnchorNode(row[4], row[5])
        beacon_a = row[8]
        beacon_b = row[9]
        calculated = found_node(anchor_a, anchor_b, beacon_a, beacon_b)

        nodes.append((*calculated, row[0], row[1]))

    return nodes



if __name__ == '__main__':
    """
    Localize nodes using only angles and anchors coords
    Use all combinations of anchors pairs ang get average coords to better precise
    """
    nodes = find_all_nodes(SIMULATED_DATA_FILE_NAME)

    for node in nodes:
        plt.plot(node[0], node[1], 'r x')       # triangulation
        plt.plot(node[2], node[3], 'b o')       # real data

    plt.show()

