import math
import numpy as np
import matplotlib.pyplot as plt
import random

from globals import TRIANGULATION_SIMULATED_DATA, NODES_COUNT, ANCHOR_STANDART_DEVIATION
from vector import Vector


def make_plot_from_csv(file):
    data = np.loadtxt(file, delimiter='\t', skiprows=1)
    nodes_coords = data[:, 0:2]
    anchors_a_coords = data[:, 2:4]#[::NODES_COUNT]
    anchors_b_coords = data[:, 4:6]#[::NODES_COUNT]
    anchors_coords = [*anchors_a_coords, *anchors_b_coords]

    plt.clf()
    for anchor in anchors_coords:
        plt.plot(anchor[0], anchor[1], 'r o')
    for node in nodes_coords:
        plt.plot(node[0], node[1], 'b o')
        
    plt.show()


def get_beacon(anchor, node):
    # angle between vector and axis X
    vector = Vector(anchor, node)
    cos = vector.x / vector.len
    phi = math.degrees(math.acos(cos))
    # process negative beacon values
    if vector.start.y < vector.end.y:
        return phi 
    else:
        return 360 - phi


def get_angles_from_nodes(anchor_a, anchor_b, node):
    # simulation
    beacon_a = get_beacon(anchor_a, node) #+ random.randint(0, ANCHOR_STANDART_DEVIATION)        # noise
    beacon_b = get_beacon(anchor_b, node) #+ random.randint(0, ANCHOR_STANDART_DEVIATION)        # noise
    beacon_a_noise = beacon_a + random.randint(0, ANCHOR_STANDART_DEVIATION)
    beacon_b_noise = beacon_b + random.randint(0, ANCHOR_STANDART_DEVIATION)

    angle1 = get_beacon(anchor_a, node) - get_beacon(anchor_a, anchor_b)
    angle2 = get_beacon(anchor_b, node) - get_beacon(anchor_b, anchor_a)
    

    return (abs(angle1), abs(angle2), beacon_a, beacon_b, beacon_a_noise, beacon_b_noise)

def get_angles_from_beacons(anchor_a, anchor_b, beacon_a, beacon_b):
    # localization
    angle_a = beacon_a - get_beacon(anchor_a, anchor_b)
    angle_b = beacon_b - get_beacon(anchor_b, anchor_a)
    return (abs(angle_a), abs(angle_b))


if __name__ == '__main__':
    with open(TRIANGULATION_SIMULATED_DATA) as file:
        make_plot_from_csv(file)