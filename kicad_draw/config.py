"""Configuration settings for KiCad PCB drawing.

This module contains default layer stackup configurations
for common PCB types used in the drawing operations.
"""

default_layers = {
    "default_4layer": {"layer_list": ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]},
    "default_6layer": {
        "layer_list": ["F.Cu", "In1.Cu", "In2.Cu", "In3.Cu", "In4.Cu", "B.Cu"]
    },
}
