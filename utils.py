import numpy as np
import matplotlib.pyplot as plt

from globals import SIMULATED_DATA_FILE_NAME, NODES_COUNT


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

if __name__ == '__main__':
    with open(SIMULATED_DATA_FILE_NAME) as file:
        make_plot_from_csv(file)