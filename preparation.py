import csv
# from proj.pg import Vector
import numpy as np
import random

from itertools import combinations

from anchor import AnchorNode
from node import Node
from globals import (CURRENT_YEAR, NODES_COUNT, ANCHORS_COUNT, ANCHOR_STANDART_DEVIATION,
                    SIMULATED_DATA_FILE_NAME, SIMULATED_DATA_COLUMNS)
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


    with open(SIMULATED_DATA_FILE_NAME, 'w', newline='') as file:
        np.savetxt(file, (SIMULATED_DATA_COLUMNS,), fmt='%15s', delimiter='\t')     # write header
        for ancor_a, ancor_b in combinations(anchors, 2):                           # all possible combinations of 2 anchors
            for node in nodes:                                                      
                row_data = node.get_simulated_data(ancor_a, ancor_b)                # collect node data (coords, anchors, angles, beacons)
                np.savetxt(file, [row_data,], fmt='%15.8f',  delimiter='\t')      
    
    print(f'\n\n[+]WRITE {NODES_COUNT * ANCHORS_COUNT} ROWS TO {SIMULATED_DATA_FILE_NAME}\n')

    make_plot_from_csv(SIMULATED_DATA_FILE_NAME)                                    # make plot
        

