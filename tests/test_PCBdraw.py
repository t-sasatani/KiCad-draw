import pytest
import filecmp
import sys
import os

from kicad_draw.PCBmodule import PCBdraw

from kicad_draw.config import default_layers

def test__can_draw_line(capsys):
    PCBdraw_ins = PCBdraw(stackup='default_4layer')
    PCBdraw_ins.drawline(x1 = 111.76, y1 = 104.14, x2 = 111.76, y2 = 108.635, line_width = 0.4, net_number=2, layer_index=0)

    result = capsys.readouterr()
    assert result.out == '(segment (start 111.76 104.14) (end 111.76 108.635) (width 0.4) (layer "F.Cu") (net 2) (tstamp 0))\n'

def test__can_draw_via(capsys):
    PCBdraw_ins = PCBdraw(stackup='default_4layer')
    PCBdraw_ins.draw_via(x = 111.76, y = 107.315, via_size=0.8, drill_size=0.4, layer_index_1 = 0, layer_index_2 = 3, net_number=2)
    result = capsys.readouterr()
    assert result.out == '(via (at 111.76 107.315) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 2) (tstamp 0))\n'

def test__can_draw_helix_coil(capsys):
    dir = os.path.dirname(__file__)
    assert_file_path = os.path.join(dir, 'assets','helix_coil_test.txt')
    out_file_path = os.path.join(dir, 'test_output', 'helix_coil_out.txt')

    sys.stdout = open(out_file_path, 'w')

    Center = [150, 100]
    track_width = 0.5
    connect_width = 0.2
    radius=11
    port_gap=0.65
    tab_gap=0.55
    via_size=0.4
    drill_size=0.2
    angle_step=0
    Nelement=100
    layerindexlist=[0,1,2,3,4,5]
    netnumber=1 # find from KiCad PCB file

    kicad_draw = PCBdraw(stackup='default_6layer')
    kicad_draw.draw_helix(x0=Center[0],
                        y0=Center[1],
                        radius=radius,
                        track_width=track_width,
                        connect_width=connect_width,
                        port_gap=port_gap,
                        net_number=netnumber,
                        drill_size=drill_size,
                        via_size=via_size,
                        tab_gap=tab_gap,
                        angle_step=angle_step,
                        layer_index_list=layerindexlist)
    
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    file1 = open(assert_file_path,'r')
    file2 = open(out_file_path,'r')

    file1_lines = file1.readlines()
    file2_lines = file2.readlines()

    for i in range(len(file1_lines)):
        try:
            assert file1_lines[i] == file2_lines[i]
        except: 
            print("Line " + str(i+1) + " doesn't match.")
            print("------------------------")
            print("File1: " + file1_lines[i])
            print("File2: " + file2_lines[i])
    file1.close()
    file2.close()
    
    #filecmp.clear_cache()
    #assert filecmp.cmp(assert_file_path, out_file_path, shallow=False)
