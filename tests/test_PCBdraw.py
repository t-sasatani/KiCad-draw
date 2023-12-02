import pytest
from kicad_draw.PCBmodule import PCBdraw

def test__can_drawline(capsys):
    PCBdraw.drawline(x1 = 111.76, y1 = 104.14, x2 = 111.76, y2 = 108.635, line_width = 0.4, LayerString = "F.Cu", net_number=2,)

    result = capsys.readouterr()
    assert result.out == '  (segment (start 111.76 104.14) (end 111.76 108.635) (width 0.4) (layer "F.Cu") (net 2) (tstamp 0))\n'

def test__can_drawvia(capsys):
    PCBdraw.drawvia(x = 111.76, y = 107.315, viasize=0.8, drillsize=0.4, Layerstring1 = "F.Cu", Layerstring2 = "B.Cu", netnumber=2)
    result = capsys.readouterr()
    assert result.out == '  (via (at 111.76 107.315) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 2) (tstamp 0))\n'