import math
import random

from globals import AOA_MAX, AOA_MIN, AXIS_Y_LIMIT, AXIS_X_LIMIT, ANCHOR_ANGLE_NOISE
from node import Node


class AnchorNode(Node):
    
    @classmethod
    def make_with_angles(cls, x, y, angles):
        anchor_node = cls(x, y)
        anchor_node.angles = angles
        return anchor_node