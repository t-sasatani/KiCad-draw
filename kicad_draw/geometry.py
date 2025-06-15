"""Geometric primitives for PCB drawing."""

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass
class Point:
    """A point in 2D space."""

    x: float
    y: float

    def __add__(self, other: "Point") -> "Point":
        """Add two points together (vector addition)."""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        """Subtract one point from another (vector subtraction)."""
        return Point(self.x - other.x, self.y - other.y)

    def rotate(self, angle: float, center: "Point") -> "Point":
        """Rotate point around center by angle in radians."""
        dx = self.x - center.x
        dy = self.y - center.y
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        return Point(
            center.x + dx * cos_angle - dy * sin_angle,
            center.y + dx * sin_angle + dy * cos_angle,
        )


@dataclass
class Line:
    """A line segment defined by two points."""

    start: Point
    end: Point
    width: float

    def to_points(self) -> Tuple[Point, Point]:
        """Return start and end points."""
        return self.start, self.end


@dataclass
class Arc:
    """An arc defined by center, radius, and angles."""

    center: Point
    radius: float
    start_angle: float
    end_angle: float
    width: float

    def to_points(self, segments: int = 100) -> List[Point]:
        """Convert arc to a list of points."""
        angles = np.linspace(self.start_angle, self.end_angle, segments + 1)
        return [
            Point(
                self.center.x + self.radius * np.cos(angle),
                self.center.y + self.radius * np.sin(angle),
            )
            for angle in angles
        ]


@dataclass
class Via:
    """A via defined by position and dimensions."""

    position: Point
    size: float
    drill_size: float
