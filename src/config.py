"""
Module with all drawing configuration
"""

# The canvas size in number of pixels. Note that the algorithm scales quadratically with this constant.
CANVAS_SIZE = 100

# Each rectangle has a long and a short side. The long side is called the length, the short side is called the width.
# These four number mark the range from which these lengths and widths are taken randomly.
MIN_LENGTH = 0.6 * CANVAS_SIZE
MAX_LENGTH = CANVAS_SIZE
MIN_WIDTH = 0.05 * CANVAS_SIZE
MAX_WIDTH = 0.2 * CANVAS_SIZE

# Amount of rectangles to draw. Note that the algorithm scales linearly with this number.
NR_RECTANGLES = 10

# Flag that indicates whether all rectangles should be fully enclosed by the canvas (True),
# or can overlap with the canvas's edge (False)
ALL_RECTANGLES_FULLY_ON_CANVAS = False
