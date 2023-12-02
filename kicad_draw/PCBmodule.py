import numpy as np
from typing import Literal

from kicad_draw.config import default_layers

class PCBdraw:
    """ Python module for generating traces for KiCad PCB.

    Args:
        layer_list (Literal["default_4layer", "default_6layer"]): layer stackup of the board.

    """
    #def __init__(self, Nlayer, net_number, track_width = 0.2, connect_width = 0.15, Nelement = 100, via_size = 0.3, drill_size = 0.15):
    def __init__(self, stackup: Literal[tuple(list(default_layers))]):
        self.layer_list = default_layers[stackup]["layer_list"]
        
    def drawline(self,
                 x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 line_width: float,
                 net_number: int,
                 layer_index: int
                 ) -> None:
        """ draw linear conductive trace

        Args:
            x1 (float): x-coordinate of start point
            y1 (float): y-coordinate of start point
            x2 (float): x-coordinate of end point
            y2 (float): y-coordinate of end point
            line_width (float): width of trace
            net_number (int): index of net
            layer_index (int): index of layer
        
        Returns:
            None

        Raises:
            AssertationError: when layer index exceeds len(layer_list)

        Example:
            >>> PCBdraw_ins = PCBdraw(stackup='default_4layer')
            >>> PCBdraw_ins.drawline(x1 = 111.76, y1 = 104.14, x2 = 111.76, y2 = 108.635, line_width = 0.4, net_number=2, layer_index=0)
              (segment (start 111.76 104.14) (end 111.76 108.635) (width 0.4) (layer "F.Cu") (net 2) (tstamp 0))

        Note:
            Example KiCad line: (segment (start 111.76 104.14) (end 111.76 108.635) (width 0.4) (layer "F.Cu") (net 2) (tstamp eada3255-4488-4dee-bc05-f72f23e4845a))
        
        """

        try:        
            assert layer_index < len(self.layer_list)
        except AssertionError as e:
            print(f'layer_index exceeds layer_list: {e}')
        layer_name = self.layer_list[layer_index]

        print("  (segment (start " + str(x1) + " " + str(y1) + ") (end " + str(x2) + " " + str(y2) + ") (width " + str(line_width) + ") (layer \"" + layer_name + "\") (net " + str(net_number) + ") (tstamp 0))")

    def draw_polyline_arc(self, x0: float, y0: float, radius: float, port_angle: float, layer_index: int, net_number: int, line_width: float, angle_offset: float = 0, segment_number: int = 100) -> None:
        """ draw arc-shaped conductive trace

        Args:
            x0 (float): x-coordinate of arc center
            y0 (float): y-coordinate of arc center
            radius (float): radius of arc
            port_angle (float): angle of arc opening
            layer_index (int): index of layer
            net_number (int): index of net
            line_width (float): width of trace
            angle_offset (float): offset of start angle of arc (default: 0)
            segment_number (int): number of segments of circle (default: 100)
        
        Returns:
            None
            
        """

        delta_angle = (2 * np.pi - port_angle)/segment_number
        for i in range(segment_number):
            x1 = x0 + radius * np.cos(port_angle/2 + i * delta_angle + angle_offset)
            x2 = x0 + radius * np.cos(port_angle/2 + (i + 1) * delta_angle + angle_offset)
            y1 = y0 + radius * np.sin(port_angle/2 + i * delta_angle + angle_offset)
            y2 = y0 + radius * np.sin(port_angle/2 + (i + 1) * delta_angle + angle_offset)
            self.drawline(x1=x1, y1=y1, x2=x2, y2=y2, line_width=line_width, layer_index=layer_index, net_number=net_number)

    def draw_via(self,
                 x: float,
                 y: float,
                 via_size: float,
                 drill_size: float,
                 net_number: int,
                 layer_index_1: int,
                 layer_index_2: int
                 ) -> None:
        """ draw via

        Args:
            x (float): x-coordinate of via
            y (float): y-coordinate of via
            via_size (float): size of via
            drill_size (float): size of drill
            net_number (int): index of net
            layer_index_1 (int): index of via start layer
            layer_index_2 (int): index of via end layer
        
        Returns:
            None
        
        Example:
            >>> PCBdraw_ins = PCBdraw(stackup='default_4layer')
            >>> PCBdraw_ins.draw_via(x = 111.76, y = 107.315, via_size=0.8, drill_size=0.4, layer_index_1 = 0, layer_index_2 = 3, net_number=2)
              (via (at 111.76 107.315) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 2) (tstamp 0))

        Note:
            Example KiCad via: (via (at 111.76 107.315) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 2) (tstamp 80a9442a-0307-48dc-b6c5-b41ea99e0e84))

        Raises:
            AssertationError: when layer index exceeds len(layer_list)
                    
        """

        try:        
            assert layer_index_1 < len(self.layer_list)
            assert layer_index_2 < len(self.layer_list)
        except AssertionError as e:
            print(f'layer_index_i exceeds layer_list: {e}')

        layer_names = [self.layer_list[layer_index_1], self.layer_list[layer_index_2]]

        print("  (via (at "+ str(x) +" "+ str(y) +") (size " + str(via_size) + ") (drill "+ str(drill_size) +") (layers \""+layer_names[0]+"\" \""+layer_names[1]+"\") (net " + str(net_number) + ") (tstamp 0))")

    def draw_helix(self, x0: float,
                   y0: float,
                   radius: float,
                   port_gap: float,
                   tab_gap: float,
                   angle_step: float,
                   layer_index_list: list,
                   track_width: float,
                   connect_width: float,
                   drill_size: float,
                   via_size: float,
                   net_number: int,
                   tab_position: Literal['IN','OUT'] = 'OUT',
                   base_angle_offset: float = 0,
                   segment_number: int = 100
                   ) -> None:
        """ draw helix coil pattern

        Args:
            x0 (float): x-coordinate of helix coil center
            y0 (float): y-coordinate of helix coil center
            radius (float): radius of helix coil
            portgap (float): length of port opening
            tabgap (float): TBD
            angle_step: TBD
            layer_index_list (list): list/order of layers to draw helix coil
            track_width (float): width of trace
            track_width (float): width of connection trace
            tab_position (string): defines position of tab for placing vias (not working yet)
            drill_size (float): size of via in drill
            via_size (float): size of via
            net_number (int): index of net
            base_angle_offset (float): defines starting angle offset
            segment_number (int): number of segments of circle (default: 100)

        Returns:
            None
            
        Raises:
            AssertationError: when layer index exceeds len(layer_list)

        """
        #angle of the port openings
        port_angle = np.arcsin(port_gap/2/radius) * 2

        #draw coil patterns
        for turn in range(len(layer_index_list)):
            turn_angle_offset = (port_angle+angle_step)*turn + base_angle_offset - (port_angle+angle_step)*(len(layer_index_list)-1)/2
            self.draw_polyline_arc(x0=x0,
                                  y0=y0,
                                  radius=radius,
                                  port_angle=port_angle,
                                  line_width=track_width,
                                  layer_index=layer_index_list[turn],
                                  net_number=net_number,
                                  angle_offset=turn_angle_offset,
                                  segment_number=segment_number)

            port_angle_top = turn_angle_offset + port_angle/2
            port_angle_bottom = turn_angle_offset - port_angle/2

            x1_top = x0 + radius * np.cos(port_angle_top)
            y1_top = y0 + radius * np.sin(port_angle_top)
            x2_top = x0 + (radius + tab_gap) * np.cos(port_angle_top + angle_step/2)
            y2_top = y0 + (radius + tab_gap) * np.sin(port_angle_top + angle_step/2)
            
            x1_bottom = x0 + radius * np.cos(port_angle_bottom)
            y1_bottom = y0 + radius * np.sin(port_angle_bottom)
            x2_bottom = x0 + (radius + tab_gap) * np.cos(port_angle_bottom - angle_step/2)
            y2_bottom = y0 + (radius + tab_gap) * np.sin(port_angle_bottom - angle_step/2)

            if turn != 0:
                self.drawline (x1=x1_bottom,
                                y1=y1_bottom,
                                x2=x2_bottom,
                                y2=y2_bottom,
                                line_width=connect_width,
                                layer_index=layer_index_list[turn],
                                net_number=net_number
                                )
            if turn != len(layer_index_list) - 1:
                self.drawline (x1=x1_top,
                                y1=y1_top,
                                x2=x2_top,
                                y2=y2_top,
                                line_width=connect_width,
                                layer_index=layer_index_list[turn],
                                net_number=net_number
                                )
                self.draw_via(x=x2_top,
                              y=y2_top,
                              drill_size=drill_size,
                              via_size=via_size,
                              layer_index_1=layer_index_list[turn],
                              layer_index_2=layer_index_list[turn+1],
                              net_number=net_number
                              )

    def open_pcbfile(self, path):
        """ open pcb file **(not used yet)**

        Args:
            path (str): path to .kicad_pcb file
        
        Returns:
            None

        Raises:
            FileNotFoundError: if file is not found
            
        """
        try:
            self.file = open(path , "r+")
        except FileNotFoundError:
            # doesn’t exist
            print('File doesn\'t exit')
        else:
            # exists
            print('opened:' + path)

    '''
    def drawspiral_2layer(self, x0, y0, rstart, rend, Nturns, Portgap, Nelement, layer_index1, layer_index2, TrackWidth, Connectwidth, net_number):
        r_inc = (rend - rstart)/(Nturns-1)
        for i in range(Nturns):
            self.draw_polyline_arc(x0, y0, rstart + r_inc * i, Portgap, Nelement, self.layers[layer_index1], TrackWidth, net_number)
            if i < Nturns -1:
                port_angle1 = np.arcsin((Portgap/2)/(rstart + r_inc * i))
                port_angle2 = np.arcsin((Portgap/2)/(rstart + r_inc * (i+1)))
                
                x1 = x0 + (rstart + r_inc * i) * np.cos(port_angle1)
                x2 = x0 + (rstart + r_inc * (i+1)) * np.cos(port_angle2)
                y1 = y0 + (rstart + r_inc * i) * np.sin(port_angle1)
                y2 = y0 - ((rstart + r_inc * (i+1)) * np.sin(port_angle2))
                self.drawline (x1, y1, x2, y2, Connectwidth, self.layers[layer_index1], net_number)
        for i in range(Nturns):
            self.draw_polyline_arc(x0, y0, rstart + r_inc * i, Portgap, Nelement, self.layers[layer_index2], TrackWidth, net_number)
            if i < Nturns -1:
                port_angle1 = np.arcsin((Portgap/2)/(rstart + r_inc * i))
                port_angle2 = np.arcsin((Portgap/2)/(rstart + r_inc * (i+1)))
                
                x1 = x0 + (rstart + r_inc * i) * np.cos(port_angle1)
                x2 = x0 + (rstart + r_inc * (i+1)) * np.cos(port_angle2)
                y1 = y0 - (rstart + r_inc * i) * np.sin(port_angle1)
                y2 = y0 + ((rstart + r_inc * (i+1)) * np.sin(port_angle2))
                self.drawline (x1, y1, x2, y2, Connectwidth, self.layers[layer_index2], net_number)
    '''
