"""Tests for the modern PCBmodule functionality.

This module contains comprehensive tests for the refactored PCBdraw class
including new features like visualization and parameter models.
"""

import pytest

from kicad_draw.models import HelixParams, HelixRectangleParams
from kicad_draw.PCBmodule import PCBdraw


@pytest.fixture
def pcb_4layer():
    """Fixture to create a PCBdraw instance with a 4-layer stackup."""
    return PCBdraw("default_4layer")


@pytest.fixture
def pcb_4layer_file():
    """Create a PCBdraw instance with 4-layer stackup in file mode for testing."""
    return PCBdraw("default_4layer", mode="file")


def test_drawline(pcb_4layer_file):
    """Test drawing a line."""
    pcb_4layer_file.drawline(
        x1=111.76,
        y1=104.14,
        x2=111.76,
        y2=108.635,
        line_width=0.4,
        net_number=2,
        layer_index=0,
    )
    assert len(pcb_4layer_file.elements) == 1
    assert "segment" in pcb_4layer_file.elements[0]
    assert "F.Cu" in pcb_4layer_file.elements[0]


def test_draw_via(pcb_4layer_file):
    """Test drawing a via."""
    pcb_4layer_file.draw_via(
        x=111.76,
        y=107.315,
        via_size=0.8,
        drill_size=0.4,
        layer_index_1=0,
        layer_index_2=3,
        net_number=2,
    )
    assert len(pcb_4layer_file.elements) == 1
    assert "via" in pcb_4layer_file.elements[0]
    assert "F.Cu" in pcb_4layer_file.elements[0]
    assert "B.Cu" in pcb_4layer_file.elements[0]


def test_draw_polyline_arc(pcb_4layer_file):
    """Test drawing a polyline arc."""
    pcb_4layer_file.draw_polyline_arc(
        x0=150.0,
        y0=100.0,
        radius=10.0,
        port_angle=0.5,
        layer_index=0,
        net_number=1,
        line_width=0.5,
        segment_number=10,
    )
    # Should generate multiple line segments
    assert len(pcb_4layer_file.elements) == 10
    for element in pcb_4layer_file.elements:
        assert "segment" in element
        assert "F.Cu" in element


def test_draw_helix(pcb_4layer_file):
    """Test drawing a helix with new HelixParams API."""
    params = HelixParams(
        x0=150.0,
        y0=100.0,
        radius=10.0,
        port_gap=1.0,
        tab_gap=2.0,
        angle_step=0.1,
        layer_index_list=[0, 1],
        track_width=0.5,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
        segment_number=10,
    )

    pcb_4layer_file.draw_helix(params)

    # Should generate segments and vias
    assert len(pcb_4layer_file.elements) > 0
    # Check that we have both segments and vias
    segments = [e for e in pcb_4layer_file.elements if "segment" in e]
    vias = [e for e in pcb_4layer_file.elements if "via" in e]
    assert len(segments) > 0
    assert len(vias) > 0


def test_draw_helix_with_params(pcb_4layer_file):
    """Test drawing a helix with new HelixParams interface."""
    params = HelixParams(
        x0=150.0,
        y0=100.0,
        radius=10.0,
        port_gap=1.0,
        tab_gap=2.0,
        angle_step=0.1,
        layer_index_list=[0, 1],
        track_width=0.5,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
        segment_number=10,
    )

    pcb_4layer_file.draw_helix(params=params)

    # Should generate segments and vias
    assert len(pcb_4layer_file.elements) > 0
    # Check that we have both segments and vias
    segments = [e for e in pcb_4layer_file.elements if "segment" in e]
    vias = [e for e in pcb_4layer_file.elements if "via" in e]
    assert len(segments) > 0
    assert len(vias) > 0


def test_visualize_exported_instance():
    """Test visualizing a PCB instance after export (reconstruction from s-expressions)."""
    # Create PCB without visualization initially enabled
    pcb = PCBdraw("default_4layer", mode="file", enable_visualization=False)

    # Draw some elements
    pcb.drawline(x1=0, y1=0, x2=10, y2=10, line_width=0.5, net_number=1, layer_index=0)
    pcb.draw_via(
        x=5,
        y=5,
        via_size=0.8,
        drill_size=0.4,
        layer_index_1=0,
        layer_index_2=1,
        net_number=1,
    )

    # Export to s-expressions
    s_expressions = pcb.export()
    assert len(s_expressions) > 0
    assert len(pcb.elements) == 2

    # Now visualize the exported instance - should reconstruct from s-expressions
    svg_content = pcb.visualize(visible_layers=[0, 1], show_vias=True)

    # Should generate valid SVG content
    assert len(svg_content) > 0
    assert "<svg" in svg_content
    assert "</svg>" in svg_content

    # Should contain visual elements
    assert "line" in svg_content or "path" in svg_content  # Lines/traces
    assert "circle" in svg_content  # Vias


def test_invalid_layer_index(pcb_4layer_file):
    """Test that invalid layer index raises appropriate error."""
    with pytest.raises(ValueError, match="Invalid layer index: 10"):
        pcb_4layer_file.drawline(
            x1=0, y1=0, x2=1, y2=1, line_width=0.5, net_number=1, layer_index=10
        )


def test_draw_helix_rectangle(pcb_4layer_file):
    """Test drawing a rectangular helix."""
    params = HelixRectangleParams(
        x0=150.0,
        y0=100.0,
        width=30.0,
        height=20.0,
        corner_radius=3.0,
        layer_index_list=[0, 1],
        track_width=0.5,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
    )

    pcb_4layer_file.draw_helix_rectangle(params)

    # Should generate multiple elements
    assert len(pcb_4layer_file.elements) > 0
    # Check that we have segments
    segments = [e for e in pcb_4layer_file.elements if "segment" in e]
    assert len(segments) > 0


def test_draw_helix_rectangle_with_ports(pcb_4layer_file):
    """Test drawing a rectangular helix with ports."""
    params = HelixRectangleParams(
        x0=150.0,
        y0=100.0,
        width=30.0,
        height=20.0,
        corner_radius=3.0,
        layer_index_list=[0, 1],
        track_width=0.5,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
        port_gap=2.0,
        tab_gap=3.0,
    )

    pcb_4layer_file.draw_helix_rectangle(params)

    # Should generate multiple elements including vias for layer connections
    assert len(pcb_4layer_file.elements) > 0
    segments = [e for e in pcb_4layer_file.elements if "segment" in e]
    vias = [e for e in pcb_4layer_file.elements if "via" in e]
    assert len(segments) > 0
    assert len(vias) > 0


def test_mode_switch():
    """Test switching between print and file modes."""
    pcb = PCBdraw("default_4layer", mode="print")
    assert pcb.mode == "print"

    pcb.set_mode("file")
    assert pcb.mode == "file"

    pcb.drawline(x1=0, y1=0, x2=1, y2=1, line_width=0.5, net_number=1, layer_index=0)
    assert len(pcb.elements) == 1
