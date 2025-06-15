import pytest

from kicad_draw.models import HelixRectangleParams
from kicad_draw.PCBmodule import PCBdraw


@pytest.fixture
def pcb_4layer():
    """Fixture to create a PCBdraw instance with a 4-layer stackup."""
    return PCBdraw("default_4layer")


@pytest.fixture
def pcb_4layer_file():
    return PCBdraw("default_4layer", mode="file")


def test_drawline(pcb_4layer, capsys):
    """Test drawing a line."""
    pcb_4layer.drawline(
        x1=100.0,
        y1=100.0,
        x2=200.0,
        y2=100.0,
        line_width=0.4,
        net_number=1,
        layer_index=0,
    )
    captured = capsys.readouterr()
    assert (
        '(segment (start 100.0 100.0) (end 200.0 100.0) (width 0.4) (layer "F.Cu") (net 1) (tstamp 0))'
        in captured.out
    )


def test_draw_via(pcb_4layer, capsys):
    """Test drawing a via."""
    pcb_4layer.draw_via(
        x=100.0,
        y=100.0,
        via_size=0.4,
        drill_size=0.2,
        net_number=1,
        layer_index_1=0,
        layer_index_2=1,
    )
    captured = capsys.readouterr()
    assert (
        '(via (at 100.0 100.0) (size 0.4) (drill 0.2) (layers "F.Cu" "In1.Cu") (net 1) (tstamp 0))'
        in captured.out
    )


def test_draw_polyline_arc(pcb_4layer, capsys):
    """Test drawing a polyline arc."""
    pcb_4layer.draw_polyline_arc(
        x0=100.0,
        y0=100.0,
        radius=50.0,
        port_angle=0.5,
        layer_index=0,
        net_number=1,
        line_width=0.4,
    )
    captured = capsys.readouterr()
    assert "(segment (start" in captured.out


def test_draw_helix(pcb_4layer, capsys):
    """Test drawing a helix."""
    pcb_4layer.draw_helix(
        x0=100.0,
        y0=100.0,
        radius=50.0,
        port_gap=10.0,
        tab_gap=5.0,
        angle_step=0.1,
        layer_index_list=[0, 1],
        track_width=0.4,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
    )
    captured = capsys.readouterr()
    assert "(segment (start" in captured.out


def test_invalid_layer_index(pcb_4layer):
    """Test drawing with invalid layer index."""
    with pytest.raises(ValueError, match="Invalid layer index: 10"):
        pcb_4layer.drawline(
            x1=100.0,
            y1=100.0,
            x2=200.0,
            y2=100.0,
            line_width=0.4,
            net_number=1,
            layer_index=10,  # Invalid layer index
        )


def test_draw_helix_rectangle(pcb_4layer, capsys):
    """Test drawing a helix rectangle."""
    params = HelixRectangleParams(
        x0=100.0,
        y0=100.0,
        width=50.0,
        height=30.0,
        corner_radius=5.0,
        layer_index_list=[0, 1],
        track_width=0.4,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
    )
    pcb_4layer.draw_helix_rectangle(params)
    captured = capsys.readouterr()
    assert "(segment (start" in captured.out
    assert "(via (at" in captured.out


def test_draw_helix_rectangle_with_ports(pcb_4layer, capsys):
    """Test drawing a helix rectangle with ports."""
    params = HelixRectangleParams(
        x0=100.0,
        y0=100.0,
        width=50.0,
        height=30.0,
        corner_radius=5.0,
        layer_index_list=[0, 1, 2],
        track_width=0.4,
        connect_width=0.3,
        drill_size=0.2,
        via_size=0.4,
        net_number=1,
        port_gap=2.0,
        tab_gap=3.0,
    )
    pcb_4layer.draw_helix_rectangle(params)
    captured = capsys.readouterr()
    assert "(segment (start" in captured.out
    assert "(via (at" in captured.out
    # Should have more segments due to port gaps and tabs
    segment_count = captured.out.count("(segment")
    assert segment_count > 20  # Should have many segments for the complex shape


def test_mode_switch(pcb_4layer):
    """Test switching between print and file modes."""
    # Start in print mode
    assert pcb_4layer.mode == "print"

    # Switch to file mode
    pcb_4layer.set_mode("file")
    assert pcb_4layer.mode == "file"
    assert len(pcb_4layer.elements) == 0  # Buffer should be empty

    # Draw something
    pcb_4layer.drawline(
        x1=100.0,
        y1=100.0,
        x2=200.0,
        y2=100.0,
        line_width=0.4,
        net_number=1,
        layer_index=0,
    )
    assert len(pcb_4layer.elements) == 1  # Should have one element

    # Switch back to print mode
    pcb_4layer.set_mode("print")
    assert pcb_4layer.mode == "print"
    assert len(pcb_4layer.elements) == 0  # Buffer should be cleared
