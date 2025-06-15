"""Constants for KiCad-draw library.

This module contains all mathematical and geometric constants used throughout
the library for PCB coil generation and visualization.
"""

from enum import IntEnum

import numpy as np


class Math:
    """Mathematical constants."""

    HALF_DIVISOR = 2
    DOUBLE_MULTIPLIER = 2


class Geometry:
    """Geometric constants."""

    PORT_SPACING_UNIT = 1.0
    RECTANGLE_SIDES_COUNT = 4


class RectangleIndex(IntEnum):
    """Rectangle side and corner indices."""

    BOTTOM_SIDE = 0
    RIGHT_SIDE = 1
    TOP_SIDE = 2
    LEFT_SIDE = 3

    # Corners use same indices as sides
    BOTTOM_LEFT_CORNER = 0
    BOTTOM_RIGHT_CORNER = 1
    TOP_RIGHT_CORNER = 2
    TOP_LEFT_CORNER = 3


class Angle:
    """Angle constants."""

    ZERO = 0
    PI = np.pi
    HALF_PI = np.pi / 2
    THREE_HALF_PI = 3 * np.pi / 2
    TWO_PI = 2 * np.pi


class Defaults:
    """Default parameter values."""

    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600
    SEGMENT_COUNT = 100
    ARC_SEGMENTS = 32
    LEGEND_MARGIN = 50  # pixels
    LEGEND_X = 20
    LEGEND_Y = 30
