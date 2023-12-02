import pytest
from kicad_draw.PCBmodule import PCBdraw

from kicad_draw.config import default_layers

def test__can_draw_line(capsys):
    PCBdraw_ins = PCBdraw(stackup='default_4layer')
    PCBdraw_ins.drawline(x1 = 111.76, y1 = 104.14, x2 = 111.76, y2 = 108.635, line_width = 0.4, net_number=2, layer_index=0)

    result = capsys.readouterr()
    assert result.out == '  (segment (start 111.76 104.14) (end 111.76 108.635) (width 0.4) (layer "F.Cu") (net 2) (tstamp 0))\n'

def test__can_draw_via(capsys):
    PCBdraw_ins = PCBdraw(stackup='default_4layer')
    PCBdraw_ins.draw_via(x = 111.76, y = 107.315, via_size=0.8, drill_size=0.4, layer_index_1 = 0, layer_index_2 = 3, net_number=2)
    result = capsys.readouterr()
    assert result.out == '  (via (at 111.76 107.315) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 2) (tstamp 0))\n'