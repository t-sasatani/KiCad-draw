#!/usr/bin/env python3
"""
Script to generate SVG examples for documentation.
This creates various SVG visualizations showing the capabilities of KiCad-draw.
"""

import os
import sys

# Add the parent directory to path so we can import kicad_draw
sys.path.insert(0, os.path.abspath(".."))

from kicad_draw.models import HelixParams, HelixRectangleParams
from kicad_draw.PCBmodule import PCBdraw


def ensure_images_dir():
    """Ensure the _static/images directory exists for SVG files."""
    images_dir = os.path.join("_static", "images")
    os.makedirs(images_dir, exist_ok=True)
    return images_dir


def generate_circular_helix_example():
    """Generate circular helix SVG example."""
    print("Generating circular helix example...")

    params = HelixParams(
        x0=150.0,
        y0=100.0,
        radius=11.0,
        port_gap=0.65,
        tab_gap=0.55,
        angle_step=0.1,
        layer_index_list=[0, 1, 2, 3],
        track_width=0.5,
        connect_width=0.2,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
        segment_number=100,
    )

    pcb = PCBdraw(stackup="default_6layer", mode="file")
    pcb.draw_helix(params)

    # Generate SVG with different layer combinations
    images_dir = ensure_images_dir()

    # All layers visible
    svg_content = pcb.visualize(visible_layers=[0, 1, 2, 3], show_vias=True)
    with open(os.path.join(images_dir, "circular_helix_all_layers.svg"), "w") as f:
        f.write(svg_content)

    # Only F.Cu and B.Cu visible
    svg_content = pcb.visualize(visible_layers=[0, 3], show_vias=True)
    with open(os.path.join(images_dir, "circular_helix_outer_layers.svg"), "w") as f:
        f.write(svg_content)

    print("✅ Circular helix examples generated")


def generate_rectangular_helix_example():
    """Generate rectangular helix SVG example."""
    print("Generating rectangular helix example...")

    params = HelixRectangleParams(
        x0=150.0,
        y0=100.0,
        width=30.0,
        height=20.0,
        corner_radius=3.0,
        layer_index_list=[0, 1, 2, 3],
        track_width=0.5,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
        port_gap=0.65,
        tab_gap=0.55,
    )

    pcb = PCBdraw(stackup="default_6layer", mode="file")
    pcb.draw_helix_rectangle(params)

    images_dir = ensure_images_dir()

    # All layers visible
    svg_content = pcb.visualize(visible_layers=[0, 1, 2, 3], show_vias=True)
    with open(os.path.join(images_dir, "rectangular_helix_all_layers.svg"), "w") as f:
        f.write(svg_content)

    # Only F.Cu and B.Cu visible
    svg_content = pcb.visualize(visible_layers=[0, 3], show_vias=True)
    with open(os.path.join(images_dir, "rectangular_helix_outer_layers.svg"), "w") as f:
        f.write(svg_content)

    print("✅ Rectangular helix examples generated")


def generate_comparison_example():
    """Generate a side-by-side comparison."""
    print("Generating comparison example...")

    # Simple example for comparison
    circular_params = HelixParams(
        x0=100.0,
        y0=100.0,
        radius=8.0,
        port_gap=0.5,
        tab_gap=0.4,
        angle_step=0.0,
        layer_index_list=[0, 1],
        track_width=0.5,
        connect_width=0.2,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
    )

    rectangular_params = HelixRectangleParams(
        x0=200.0,
        y0=100.0,
        width=20.0,
        height=16.0,
        corner_radius=2.0,
        layer_index_list=[0, 1],
        track_width=0.5,
        connect_width=0.2,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
        port_gap=0.5,
        tab_gap=0.4,
    )

    pcb = PCBdraw(stackup="default_4layer", mode="file")
    pcb.draw_helix(circular_params)
    pcb.draw_helix_rectangle(rectangular_params)

    images_dir = ensure_images_dir()
    svg_content = pcb.visualize(visible_layers=[0, 1], show_vias=True)
    with open(
        os.path.join(images_dir, "comparison_circular_vs_rectangular.svg"), "w"
    ) as f:
        f.write(svg_content)

    print("✅ Comparison example generated")


if __name__ == "__main__":
    print("Generating SVG examples for documentation...")
    generate_circular_helix_example()
    generate_rectangular_helix_example()
    generate_comparison_example()
    print("\n🎉 All SVG examples generated successfully!")
    print("Files saved in docs/_static/images/")
