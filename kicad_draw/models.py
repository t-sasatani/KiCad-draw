"""Data models for KiCad PCB drawing parameters.

This module contains Pydantic models that define the parameters
for various PCB drawing operations, ensuring type safety and validation.
"""

from typing import List

from pydantic import BaseModel


class HelixRectangleParams(BaseModel):
    """Parameters for drawing rectangular helix coil patterns.

    This model defines all the geometric and electrical parameters
    needed to generate a rectangular helix coil on a PCB, including
    dimensions, layer configuration, and connection details.

    Attributes:
        x0: X-coordinate of the rectangle center (mm)
        y0: Y-coordinate of the rectangle center (mm)
        width: Width of the rectangle (mm)
        height: Height of the rectangle (mm)
        corner_radius: Radius for rounded corners (mm)
        layer_index_list: List of layer indices for the helix (0=F.Cu, 1=In1.Cu, etc.)
        track_width: Width of the main coil traces (mm)
        connect_width: Width of the connection traces between layers (mm)
        drill_size: Diameter of via drill holes (mm)
        via_size: Outer diameter of vias (mm)
        net_number: KiCad net number for electrical connectivity
        segment_number: Number of segments for curved sections (default: 100)
        port_gap: Gap size for ports in mm (0 means no ports, default: 0.0)
        tab_gap: Extension distance for connection tabs in mm (default: 0.0)

    """

    x0: float
    y0: float
    width: float
    height: float
    corner_radius: float
    layer_index_list: List[int]
    track_width: float
    connect_width: float
    drill_size: float
    via_size: float
    net_number: int
    segment_number: int = 100
    port_gap: float = 0.0  # Gap size for ports (0 means no ports)
    tab_gap: float = 0.0  # Extension distance for connection tabs
