import random
import numpy as np
import math
import matplotlib.pyplot as plt
from itertools import combinations

from globals import  NODES_COUNT, ANCHORS_COUNT, CURRENT_YEAR, LIGHT_SPEED, TOA_SIMULATED_DATA, TOA_STD_DEVIATION, SIMULATED_TOA_DATA_COLUMNS
from node import Node
from trilateration_RSSI import get_distance, node_trilateration


random.seed(CURRENT_YEAR)


class Locator(Node):
    def __init__(self, x, y, t):
        super().__init__(x, y)
        self.r = get_distance_from_time(t)
    
    def __repr__(self):
        return super().__repr__() + f"\tRad:\t{self.r}"


def get_distance_from_time(t):
    return t * LIGHT_SPEED


def get_time(d):
    return d / LIGHT_SPEED

def toa_sim(locators, nodes):
    data = []   # array of data for each point
    # node_x, node_y, a1_x, a1_y, ss1, ss_n_1, d1, a2_x, a2_y, ss2, ss_n_2, d2, a3_x, a3_y, ss3, ss_n_3, d3
    for node in nodes:
        row_data = [node.x, node.y]
        for locator in locators:
            d = get_distance(locator, node)
            toa = get_time(d)
            toa_noise = toa + random.randrange(-TOA_STD_DEVIATION, TOA_STD_DEVIATION) * pow(10, -9)

            row_data += [locator.x, locator.y, toa, toa_noise, d]
        data.append(row_data)

    return data


def simulate_and_write_toa(locators_cnt, nodes_cnt, file_name):
    locators = [Node.create_random() for _ in range(locators_cnt)]
    nodes = [Node.create_random() for _ in range(nodes_cnt)]
    data = toa_sim(locators, nodes)
    with open(file_name, 'w', newline='') as file:
        np.savetxt(file, (SIMULATED_TOA_DATA_COLUMNS,), fmt='%15s', delimiter='\t')             # write header

        for row in data:
            np.savetxt(file, [row,], fmt='%15.8f',  delimiter='\t')
    
    with open(file_name, 'r') as file:
        file_data = np.loadtxt(file, delimiter='\t', skiprows=1)
        print(f'\n\n[+]WRITE {len(file_data)} ROWS TO {file_name}\n')

    return (locators, nodes)


def find_all_nodes_rssi(file_name):
    real_nodes = []
    found_points_real = []
    found_points_noise = []
    data = np.loadtxt(file_name, delimiter='\t', skiprows=1)
    for row in data:
        real_node = Node(row[0], row[1])
        real_nodes.append(real_node)

        loc1_real = Locator(row[2], row[3], row[4])
        loc2_real = Locator(row[7], row[8], row[9])
        loc3_real = Locator(row[12], row[13], row[14])

        loc1_noise = Locator(row[2], row[3], row[5])
        loc2_noise = Locator(row[7], row[8], row[10])
        loc3_noise = Locator(row[12], row[13], row[15])

        locators_real = [loc1_real, loc2_real, loc3_real]
        locators_noise = [loc1_noise, loc2_noise, loc3_noise]

        noise_points = node_trilateration(locators_noise)
        real_points = node_trilateration(locators_real)
        found_points_real.append(real_points[-1])
        if len(noise_points) == 3:
            # take first point instead of avg
            found_points_noise.append(noise_points[0])

        else:
            found_points_noise.append(noise_points[-1])
        
    return (real_nodes, found_points_real, found_points_noise)



if __name__ == "__main__":
    locators, nodes = simulate_and_write_toa(ANCHORS_COUNT, NODES_COUNT, TOA_SIMULATED_DATA)
    result_nodes = find_all_nodes_rssi(TOA_SIMULATED_DATA)

    # locators red points
    for node in locators:
        plt.plot(node.x, node.y, 'r o')       

    # real nodes blue points
    for node in nodes:
        plt.plot(node.x, node.y, 'b o')       
    
    # calculated with deviation green X
    for node in result_nodes[2]:             
        plt.plot(node.x, node.y, 'g x')
    plt.show()

