import csv
import numpy as np
import random

from itertools import combinations

from anchor import AnchorNode
from node import Node
from globals import (CURRENT_YEAR, NODES_COUNT, ANCHORS_COUNT,
                    TRIANGULATION_SIMULATED_DATA, SIMULATED_DATA_COLUMNS)
from utils import make_plot_from_csv


random.seed(CURRENT_YEAR)


if __name__ == '__main__':
    """
    Simulate network
    write data to csv file
    show plot
    """
    anchors = [AnchorNode.create_random() for _ in range(ANCHORS_COUNT)]
    nodes = [Node.create_random() for _ in range(NODES_COUNT)]


    with open(TRIANGULATION_SIMULATED_DATA, 'w', newline='') as file:
        np.savetxt(file, (SIMULATED_DATA_COLUMNS,), fmt='%15s', delimiter='\t')             # write header
        for node in nodes:
            for anchor_a, anchor_b in combinations(anchors, 2):                             # all possible combinations of 2 anchors
                row_data = node.get_simulated_data(anchor_a, anchor_b)                      # collect node data (coords, anchors, angles, beacons)
                np.savetxt(file, [row_data,], fmt='%15.8f',  delimiter='\t')      
    
    with open(TRIANGULATION_SIMULATED_DATA, 'r') as file:
        data = np.loadtxt(file, delimiter='\t', skiprows=1)
        print(f'\n\n[+]WRITE {len(data)} ROWS TO {TRIANGULATION_SIMULATED_DATA}\n')


    make_plot_from_csv(TRIANGULATION_SIMULATED_DATA)                                        # make plot
