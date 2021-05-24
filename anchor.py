from node import Node


class AnchorNode(Node):
    @classmethod
    def make_with_angles(cls, x, y, angles):
        anchor_node = cls(x, y)
        anchor_node.angles = angles
        return anchor_node
