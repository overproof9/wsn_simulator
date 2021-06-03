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
PL0 = -36.029                   # Reference Path Loss in dB
PL_EXP = 2.386                  # Path loss Exponent
PL_D0 = 1                          # Reference Distance in Meters
PL_STD_DEVIATION = 0.5          # Noise Standard Deviation in dB
RSSI_SIMULATED_DATA = 'rssi_simulated_data.csv'
SIMULATED_RSSI_DATA_COLUMNS = ['node_x', 'node_y', 'anchor_a_x', 'anchor_a_y', 'anchor_b_x', 'anchor_b_y', 'anchor_c_x', 'anchor_c_y', 'rss_a', 'rss_b', 'rss_c']
