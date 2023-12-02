import pytest
from kicad_draw.PCBmodule import PCBdraw

def test__can_drawline(capsys):
    kicad_draw = PCBdraw(Nlayer=6, net_number=2)
    kicad_draw.drawline(x1 = 111.76, y1 = 104.14, x2 = 111.76, y2 = 108.635, line_width = 0.4, LayerString = "F.Cu")

    result = capsys.readouterr()
    assert result.out == '  (segment (start 111.76 104.14) (end 111.76 108.635) (width 0.4) (layer "F.Cu") (net 2) (tstamp 0))\n'