import numpy as np
import math
import matplotlib.pyplot as plt

from functools import reduce

from anchor import AnchorNode
from globals import NODES_COUNT, SIMULATED_DATA_FILE_NAME, ANCHORS_COUNT
from node import Node, get_angles_from_beacons


# def load_anchors(file):
#     anchors = []
#     data = np.loadtxt(file, delimiter='\t', skiprows=1)
#     anchors_coords = data[:, 2:5][::NODES_COUNT]
#     current_anchor_idx = 0
#     while current_anchor_idx < ANCHORS_COUNT:
#         start_idx = current_anchor_idx * NODES_COUNT
#         stop_idx = start_idx + NODES_COUNT
#         anchor_angles = data[start_idx:stop_idx, 4:5]
#         x = anchors_coords[current_anchor_idx][0]
#         y = anchors_coords[current_anchor_idx][1]
#         anchors.append(AnchorNode.make_with_angles(x, y, anchor_angles))
        
#         current_anchor_idx += 1
#     return anchors


# def found_nodes(anchors):
#     removed_anchor = anchors.pop()
#     row_nodes = []
#     while anchors:
#         for current_anchor in anchors:
#             nodes = []
#             distance = Node._distance(removed_anchor, current_anchor)
#             for phi_a, phi_b in zip(removed_anchor.angles, current_anchor.angles):
#                 nodes.append(Node.found_node(distance, phi_a, phi_b))
#             row_nodes.append(nodes)
#         removed_anchor = anchors.pop()
#     return row_nodes


# def get_nodes_average_coords(row_nodes):
#     nodes = []
#     for current_idx in range(len(row_nodes[0])):
#         curr_nodes = [row_nodes[i][current_idx] for i in range(len(row_nodes))]
#         nodes.append(get_average(curr_nodes))
#     return nodes


# def get_average(nodes):
#     x = sum([node.x for node in nodes]) / len(nodes)
#     y = sum([node.y for node in nodes]) / len(nodes)
#     return Node(x, y)


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
    # filtered_data = data[:, 2:8]        # get anchors and related angles to found node

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

