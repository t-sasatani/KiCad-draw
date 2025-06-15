import pytest

from kicad_draw.PCBmodule import PCBdraw


@pytest.fixture
def pcb_4layer():
    """Fixture to create a PCBdraw instance with a 4-layer stackup."""
    return PCBdraw(stackup="default_4layer")


def test_drawline(pcb_4layer, capsys):
    """Test drawing a simple line."""
    # Test drawing a simple line
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
    expected = '(segment (start 100.0 100.0) (end 200.0 100.0) (width 0.4) (layer "F.Cu") (net 1) (tstamp 0))\n'
    assert captured.out == expected


def test_draw_via(pcb_4layer, capsys):
    """Test drawing a via."""
    # Test drawing a via
    pcb_4layer.draw_via(
        x=100.0,
        y=100.0,
        via_size=0.8,
        drill_size=0.4,
        net_number=1,
        layer_index_1=0,
        layer_index_2=3,
    )
    captured = capsys.readouterr()
    expected = '(via (at 100.0 100.0) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 1) (tstamp 0))\n'
    assert captured.out == expected


def test_draw_polyline_arc(pcb_4layer, capsys):
    """Test drawing an arc."""
    # Test drawing an arc
    pcb_4layer.draw_polyline_arc(
        x0=100.0,
        y0=100.0,
        radius=50.0,
        port_angle=1.0,
        layer_index=0,
        net_number=1,
        line_width=0.4,
        angle_offset=0,
        segment_number=4,  # Using small number for testing
    )
    captured = capsys.readouterr()
    # We expect 4 segments for the arc
    lines = captured.out.strip().split("\n")
    assert len(lines) == 4
    # Check first segment
    assert lines[0].startswith("(segment (start")
    assert '(layer "F.Cu")' in lines[0]
    assert "(net 1)" in lines[0]


def test_draw_helix(pcb_4layer, capsys):
    """Test drawing a simple helix with 2 turns."""
    # Test drawing a simple helix with 2 turns
    pcb_4layer.draw_helix(
        x0=100.0,
        y0=100.0,
        radius=50.0,
        port_gap=10.0,
        tab_gap=5.0,
        angle_step=0.5,
        layer_index_list=[0, 1],
        track_width=0.4,
        connect_width=0.3,
        drill_size=0.4,
        via_size=0.8,
        net_number=1,
        segment_number=4,  # Using small number for testing
    )
    captured = capsys.readouterr()
    # We expect multiple segments for the helix
    lines = captured.out.strip().split("\n")
    assert len(lines) > 0
    # Check that we have both segments and vias
    assert any("(segment" in line for line in lines)
    assert any("(via" in line for line in lines)


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
