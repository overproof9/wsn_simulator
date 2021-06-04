import random
from numpy.lib.twodim_base import tri
from triangulation import find_all_nodes
import numpy as np
import math
import matplotlib.pyplot as plt
from itertools import combinations


from globals import PL_STD_DEVIATION, PL0, PL_EXP, PL_D0, RSSI_SIMULATED_DATA, SIMULATED_RSSI_DATA_COLUMNS, NODES_COUNT, ANCHORS_COUNT, CURRENT_YEAR
from node import Node

random.seed(CURRENT_YEAR)

class Locator(Node):
    def __init__(self, x, y, ss):
        super().__init__(x, y)
        self.r = get_radius_from_ss(ss)
    
    def __repr__(self):
        return super().__repr__() + f"\tRad:\t{self.r}"


def get_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def get_ss(d):
    # simulation
    return PL0 + (-10) * PL_EXP * math.log10(d)


def get_radius_from_ss(ss):
    #calculation
    return pow(10, (ss - PL0) / (-10*PL_EXP))


def get_intersect_points(c1, c2):
    # input 2 objects with x, y, r props
    # returns array of intersection points 
    # if no intersect = 0 elements      if 1 interserct - 1 point       if 2 then 2 points
    result = []
    rp = Node(0, 0)
    d = math.sqrt(pow(abs(c1.x - c2.x), 2) + pow(abs(c1.y - c2.y), 2))
    if (d > c1.r + c2.r):
        return result

    try:
        dtr = (c1.r**2 - c2.r**2 + d**2) / (d*2)
        h = math.sqrt(c1.r**2 - dtr**2)
    except ValueError:
        return result
    rp.x = c1.x + dtr*(c2.x - c1.x) / d
    rp.y = c1.y + dtr*(c2.y - c1.y) / d

    fx = rp.x + h*(c2.y - c1.y) / d
    fy = rp.y - h*(c2.x - c1.x) / d

    result.append(Node(fx, fy))
    if dtr == c1.r:
        return result
    
    sx = rp.x - h*(c2.y - c1.y) / d
    sy = rp.y + h*(c2.x - c1.x) / d
    result.append(Node(sx, sy))
    return result


def get_average(points):
    ax = sum(p.x for p in points) / len(points)
    ay = sum(p.y for p in points) / len(points)
    return Node(ax, ay)



def rssi_simulation(locators, nodes):
    data = []   # array of data for each point
    # node_x, node_y, a1_x, a1_y, ss1, ss_n_1, d1, a2_x, a2_y, ss2, ss_n_2, d2, a3_x, a3_y, ss3, ss_n_3, d3
    for node in nodes:
        row_data = [node.x, node.y]
        for locator in locators:
            d = get_distance(locator, node)
            ss = get_ss(d)
            ss_noise = ss + random.randrange(-PL_STD_DEVIATION *10 , PL_STD_DEVIATION * 10) / 10

            row_data += [locator.x, locator.y, ss, ss_noise, d]
        data.append(row_data)

    return data


def simulate_and_write(locators_cnt, nodes_cnt, file_name):
    locators = [Node.create_random() for _ in range(locators_cnt)]
    nodes = [Node.create_random() for _ in range(nodes_cnt)]
    data = rssi_simulation(locators, nodes)
    with open(file_name, 'w', newline='') as file:
        np.savetxt(file, (SIMULATED_RSSI_DATA_COLUMNS,), fmt='%15s', delimiter='\t')             # write header

        for row in data:
            np.savetxt(file, [row,], fmt='%15.8f',  delimiter='\t')
    
    with open(file_name, 'r') as file:
        file_data = np.loadtxt(file, delimiter='\t', skiprows=1)
        print(f'\n\n[+]WRITE {len(file_data)} ROWS TO {file_name}\n')


def node_trilateration(locators):
    # calculation
    intersection_points = []
    triangle_points = []
    for pair in combinations(locators, 2):
        intersection_points += get_intersect_points(*pair)
    # [print(el) for el in locators]
    for point in intersection_points:
        if all([point_belongs(l, point) for l in locators]):
            triangle_points.append(point)
    return triangle_points


def point_belongs(c, p):
    return (c.r + PL_STD_DEVIATION)**2 >= (p.x - c.x) ** 2 + (p.y - c.y) ** 2


def point_on_border(c, p):
    return round(c.r**2, 2) == round(((p.x - c.x) ** 2 + (p.y - c.y) ** 2), 2)


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
    simulate_and_write(ANCHORS_COUNT, NODES_COUNT, RSSI_SIMULATED_DATA)
    result_nodes = find_all_nodes_rssi(RSSI_SIMULATED_DATA)

    # real nodes
    for node in result_nodes[0]:
        
        plt.plot(node.x, node.y, 'b o')       # real data
    
    for node in result_nodes[1]:             # calculated no deviation
        plt.plot(node.x, node.y, 'r x')

    for node in result_nodes[2]:             # calculated with deviation
        plt.plot(node.x, node.y, 'g x')
    plt.show()


                
            
    