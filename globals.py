AXIS_Y_LIMIT = (0, 100)
AXIS_X_LIMIT = (0, 100)

ANCHORS_COUNT = 3


NODES_COUNT = 10


CURRENT_YEAR = 2021

# AoA
AOA_STD_DEVIATION = 5           # Degrees 
TRIANGULATION_SIMULATED_DATA = 'triangulation_simulated_data.csv'
SIMULATED_AOA_DATA_COLUMNS = ['node_x', 'node_y', 'anchor_a_x', 'anchor_a_y', 'anchor_b_x', 'anchor_b_y', 'angle_a', 'angle_b', 'beacon_a', 'beacon_b', 'beacon_a_n', 'beacon_b_n']


#RSSI
PL0 = -36                 # Reference Path Loss in dB
PL_EXP = 2.7                  # Path loss Exponent
PL_D0 = 1                          # Reference Distance in Meters
PL_STD_DEVIATION = 0.5          # Noise Standard Deviation in dB
RSSI_SIMULATED_DATA = 'rssi_simulated_data.csv'
SIMULATED_RSSI_DATA_COLUMNS = ['node_x', 'node_y', 'loc1_x', 'loc1_y', 'ss1', 'ss1_noise', 'dist1', 'loc2_x', 'loc2_y', 'ss2', 'ss2_noise', 'd2', 'loc3_x', 'loc3_y', 'ss3', 'ss3_noise', 'd3']


