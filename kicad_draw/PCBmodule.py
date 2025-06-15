"""Module for generating traces for KiCad PCB."""

from typing import List, Literal

import numpy as np

from kicad_draw.config import default_layers
from kicad_draw.formatter import KiCadFormatter
from kicad_draw.geometry import Arc, Line, Point, Via
from kicad_draw.layers import LayerManager


class PCBdraw:
    """Module for generating traces for KiCad PCB."""

    def __init__(self, stackup: Literal[tuple(list(default_layers))]):
        """Initialize the PCBdraw class with the specified stackup."""
        self.layer_manager = LayerManager(stackup)
        self.formatter = KiCadFormatter()

    def drawline(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        line_width: float,
        net_number: int,
        layer_index: int,
    ) -> None:
        """Draw linear conductive trace."""
        line = Line(
            start=Point(x1, y1),
            end=Point(x2, y2),
            width=line_width,
        )
        layer = self.layer_manager.get_layer_name(layer_index)
        print(self.formatter.format_segment(line, layer, net_number))

    def draw_polyline_arc(
        self,
        x0: float,
        y0: float,
        radius: float,
        port_angle: float,
        layer_index: int,
        net_number: int,
        line_width: float,
        angle_offset: float = 0,
        segment_number: int = 100,
    ) -> None:
        """Draw arc-shaped conductive trace."""
        center = Point(x0, y0)
        start_angle = port_angle / 2 + angle_offset
        end_angle = 2 * np.pi - port_angle / 2 + angle_offset

        arc = Arc(
            center=center,
            radius=radius,
            start_angle=start_angle,
            end_angle=end_angle,
            width=line_width,
        )

        points = arc.to_points(segment_number)
        for i in range(len(points) - 1):
            self.drawline(
                x1=points[i].x,
                y1=points[i].y,
                x2=points[i + 1].x,
                y2=points[i + 1].y,
                line_width=line_width,
                layer_index=layer_index,
                net_number=net_number,
            )

    def draw_via(
        self,
        x: float,
        y: float,
        via_size: float,
        drill_size: float,
        net_number: int,
        layer_index_1: int,
        layer_index_2: int,
    ) -> None:
        """Draw via."""
        via = Via(
            position=Point(x, y),
            size=via_size,
            drill_size=drill_size,
        )
        layers = self.layer_manager.get_layer_names([layer_index_1, layer_index_2])
        print(self.formatter.format_via(via, layers, net_number))

    def draw_helix(
        self,
        x0: float,
        y0: float,
        radius: float,
        port_gap: float,
        tab_gap: float,
        angle_step: float,
        layer_index_list: List[int],
        track_width: float,
        connect_width: float,
        drill_size: float,
        via_size: float,
        net_number: int,
        tab_position: Literal["IN", "OUT"] = "OUT",
        base_angle_offset: float = 0,
        segment_number: int = 100,
    ) -> None:
        """Draw helix coil pattern."""
        # angle of the port openings
        port_angle = np.arcsin(port_gap / 2 / radius) * 2

        # draw coil patterns
        for turn in range(len(layer_index_list)):
            turn_angle_offset = (
                (port_angle + angle_step) * turn
                + base_angle_offset
                - (port_angle + angle_step) * (len(layer_index_list) - 1) / 2
            )
            self.draw_polyline_arc(
                x0=x0,
                y0=y0,
                radius=radius,
                port_angle=port_angle,
                line_width=track_width,
                layer_index=layer_index_list[turn],
                net_number=net_number,
                angle_offset=turn_angle_offset,
                segment_number=segment_number,
            )

            port_angle_top = turn_angle_offset + port_angle / 2
            port_angle_bottom = turn_angle_offset - port_angle / 2

            x1_top = x0 + radius * np.cos(port_angle_top)
            y1_top = y0 + radius * np.sin(port_angle_top)
            x2_top = x0 + (radius + tab_gap) * np.cos(port_angle_top + angle_step / 2)
            y2_top = y0 + (radius + tab_gap) * np.sin(port_angle_top + angle_step / 2)

            x1_bottom = x0 + radius * np.cos(port_angle_bottom)
            y1_bottom = y0 + radius * np.sin(port_angle_bottom)
            x2_bottom = x0 + (radius + tab_gap) * np.cos(
                port_angle_bottom - angle_step / 2
            )
            y2_bottom = y0 + (radius + tab_gap) * np.sin(
                port_angle_bottom - angle_step / 2
            )

            if turn != 0:
                self.drawline(
                    x1=x1_bottom,
                    y1=y1_bottom,
                    x2=x2_bottom,
                    y2=y2_bottom,
                    line_width=connect_width,
                    layer_index=layer_index_list[turn],
                    net_number=net_number,
                )
            if turn != len(layer_index_list) - 1:
                self.drawline(
                    x1=x1_top,
                    y1=y1_top,
                    x2=x2_top,
                    y2=y2_top,
                    line_width=connect_width,
                    layer_index=layer_index_list[turn],
                    net_number=net_number,
                )
                self.draw_via(
                    x=x2_top,
                    y=y2_top,
                    drill_size=drill_size,
                    via_size=via_size,
                    layer_index_1=layer_index_list[turn],
                    layer_index_2=layer_index_list[turn + 1],
                    net_number=net_number,
                )

    def open_pcbfile(self, path):
        """Open pcb file **(not used yet)**."""
        try:
            self.file = open(path, "r+")
        except FileNotFoundError:
            # doesn't exist
            print("File doesn't exit")
        else:
            # exists
            print("opened:" + path)

    """
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
    """
