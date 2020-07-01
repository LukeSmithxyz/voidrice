"""Module which defines classes all about geometry"""


class Point:
    """Data class which holds a coordinate."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


class Distance:
    """Data class which holds the distance values in all directions."""
    def __init__(self, top=0, left=0, bottom=0, right=0):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
