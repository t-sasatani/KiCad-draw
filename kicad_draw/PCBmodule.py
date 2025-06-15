"""Module for generating traces for KiCad PCB."""

from typing import List, Literal, Optional

import numpy as np

from kicad_draw.config import default_layers
from kicad_draw.formatter import KiCadFormatter
from kicad_draw.geometry import Arc, Line, Point, Via
from kicad_draw.layers import LayerManager
from kicad_draw.models import HelixRectangleParams
from kicad_draw.visualizer import PCBVisualizer

# Constants for geometric calculations
HALF_DIVISOR = 2
DOUBLE_MULTIPLIER = 2
PORT_SPACING_UNIT = 1.0
RECTANGLE_SIDES_COUNT = 4

# Rectangle side indices
BOTTOM_SIDE_INDEX = 0
RIGHT_SIDE_INDEX = 1
TOP_SIDE_INDEX = 2
LEFT_SIDE_INDEX = 3

# Corner indices (same as side indices)
BOTTOM_LEFT_CORNER = 0
BOTTOM_RIGHT_CORNER = 1
TOP_RIGHT_CORNER = 2
TOP_LEFT_CORNER = 3

# Angle constants
ANGLE_PI = np.pi
ANGLE_HALF_PI = np.pi / 2
ANGLE_THREE_HALF_PI = 3 * np.pi / 2
ANGLE_TWO_PI = 2 * np.pi
ANGLE_ZERO = 0


class PCBdraw:
    """Module for generating traces for KiCad PCB."""

    def __init__(
        self,
        stackup: Literal[tuple(default_layers)],
        mode: Literal["print", "file"] = "print",
        visualizer: Optional[PCBVisualizer] = None,
    ):
        """Initialize PCBdraw with stackup.

        Args:
            stackup: The PCB stackup configuration
            mode: Operation mode - "print" for direct s-expression output, "file" for collecting elements
            visualizer: Optional PCBVisualizer instance for SVG output

        """
        self.layer_manager = LayerManager(stackup)
        self.formatter = KiCadFormatter()
        self.mode = mode
        self.elements = []  # Buffer to collect s-expressions when in file mode
        self.visualizer = visualizer

    def _output(self, s_expr: str) -> None:
        """Output s-expression based on current mode."""
        if self.mode == "print":
            print(s_expr)
        else:  # file mode
            self.elements.append(s_expr)

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
        self._output(self.formatter.format_segment(line, layer, net_number))

        # Add to visualizer if present
        if self.visualizer:
            self.visualizer.add_line(x1, y1, x2, y2, line_width, layer)

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
        self._output(self.formatter.format_via(via, layers, net_number))

        # Add to visualizer if present
        if self.visualizer:
            self.visualizer.add_via(x, y, via_size)

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
        port_angle = np.arcsin(port_gap / HALF_DIVISOR / radius) * DOUBLE_MULTIPLIER

        # draw coil patterns
        for turn in range(len(layer_index_list)):
            turn_angle_offset = (
                (port_angle + angle_step) * turn
                + base_angle_offset
                - (port_angle + angle_step) * (len(layer_index_list) - 1) / HALF_DIVISOR
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

            port_angle_top = turn_angle_offset + port_angle / HALF_DIVISOR
            port_angle_bottom = turn_angle_offset - port_angle / HALF_DIVISOR

            x1_top = x0 + radius * np.cos(port_angle_top)
            y1_top = y0 + radius * np.sin(port_angle_top)
            x2_top = x0 + (radius + tab_gap) * np.cos(
                port_angle_top + angle_step / HALF_DIVISOR
            )
            y2_top = y0 + (radius + tab_gap) * np.sin(
                port_angle_top + angle_step / HALF_DIVISOR
            )

            x1_bottom = x0 + radius * np.cos(port_angle_bottom)
            y1_bottom = y0 + radius * np.sin(port_angle_bottom)
            x2_bottom = x0 + (radius + tab_gap) * np.cos(
                port_angle_bottom - angle_step / HALF_DIVISOR
            )
            y2_bottom = y0 + (radius + tab_gap) * np.sin(
                port_angle_bottom - angle_step / HALF_DIVISOR
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

    def draw_helix_rectangle(
        self,
        params: HelixRectangleParams,
    ) -> None:
        """Draw a rectangle with rounded corners for each layer in layer_index_list.

        If port_gap > 0, creates ports (gaps) on the right side of the rectangle
        with tabs extending outward for layer connections.
        """
        corners = [
            Point(
                params.x0 - params.width / HALF_DIVISOR,
                params.y0 - params.height / HALF_DIVISOR,
            ),  # bottom-left
            Point(
                params.x0 + params.width / HALF_DIVISOR,
                params.y0 - params.height / HALF_DIVISOR,
            ),  # bottom-right
            Point(
                params.x0 + params.width / HALF_DIVISOR,
                params.y0 + params.height / HALF_DIVISOR,
            ),  # top-right
            Point(
                params.x0 - params.width / HALF_DIVISOR,
                params.y0 + params.height / HALF_DIVISOR,
            ),  # top-left
        ]

        for turn, layer_index in enumerate(params.layer_index_list):
            # Calculate port positions if ports are enabled
            if params.port_gap > 0:
                # Calculate port offset for this layer (stagger ports between layers)
                port_offset = (params.port_gap + PORT_SPACING_UNIT) * turn - (
                    params.port_gap + PORT_SPACING_UNIT
                ) * (len(params.layer_index_list) - 1) / HALF_DIVISOR

                # Port positions on the right side
                port_top_y = params.y0 + port_offset + params.port_gap / HALF_DIVISOR
                port_bottom_y = params.y0 + port_offset - params.port_gap / HALF_DIVISOR

                # Clamp ports to be within the rectangle bounds
                port_top_y = min(
                    port_top_y,
                    params.y0 + params.height / HALF_DIVISOR - params.corner_radius,
                )
                port_bottom_y = max(
                    port_bottom_y,
                    params.y0 - params.height / HALF_DIVISOR + params.corner_radius,
                )

                # Tab positions (extending horizontally outward from ports)
                tab_x = params.x0 + params.width / HALF_DIVISOR + params.tab_gap

            # Draw the four sides of the rectangle (shortened to connect with arcs)
            for i in range(RECTANGLE_SIDES_COUNT):
                start = corners[i]
                end = corners[(i + 1) % RECTANGLE_SIDES_COUNT]

                if i == BOTTOM_SIDE_INDEX:  # Bottom side
                    # Shorten by corner radius on both ends
                    start_x = start.x + params.corner_radius
                    end_x = end.x - params.corner_radius
                    self.drawline(
                        x1=start_x,
                        y1=start.y,
                        x2=end_x,
                        y2=end.y,
                        line_width=params.track_width,
                        layer_index=layer_index,
                        net_number=params.net_number,
                    )
                elif i == RIGHT_SIDE_INDEX:  # Right side
                    if params.port_gap > 0:
                        # Draw bottom part of right side (from bottom-right corner to bottom port)
                        if port_bottom_y > start.y + params.corner_radius:
                            self.drawline(
                                x1=start.x,
                                y1=start.y + params.corner_radius,
                                x2=start.x,
                                y2=port_bottom_y,
                                line_width=params.track_width,
                                layer_index=layer_index,
                                net_number=params.net_number,
                            )

                        # Draw top part of right side (from top port to top-right corner)
                        if port_top_y < end.y - params.corner_radius:
                            self.drawline(
                                x1=start.x,
                                y1=port_top_y,
                                x2=start.x,
                                y2=end.y - params.corner_radius,
                                line_width=params.track_width,
                                layer_index=layer_index,
                                net_number=params.net_number,
                            )
                    else:
                        # Normal right side, shortened by corner radius on both ends
                        self.drawline(
                            x1=start.x,
                            y1=start.y + params.corner_radius,
                            x2=end.x,
                            y2=end.y - params.corner_radius,
                            line_width=params.track_width,
                            layer_index=layer_index,
                            net_number=params.net_number,
                        )
                elif i == TOP_SIDE_INDEX:  # Top side
                    # Shorten by corner radius on both ends
                    start_x = start.x - params.corner_radius
                    end_x = end.x + params.corner_radius
                    self.drawline(
                        x1=start_x,
                        y1=start.y,
                        x2=end_x,
                        y2=end.y,
                        line_width=params.track_width,
                        layer_index=layer_index,
                        net_number=params.net_number,
                    )
                elif i == LEFT_SIDE_INDEX:  # Left side
                    # Shorten by corner radius on both ends
                    self.drawline(
                        x1=start.x,
                        y1=start.y - params.corner_radius,
                        x2=end.x,
                        y2=end.y + params.corner_radius,
                        line_width=params.track_width,
                        layer_index=layer_index,
                        net_number=params.net_number,
                    )

            # Draw rounded corners
            for i in range(RECTANGLE_SIDES_COUNT):
                corner = corners[i]
                if i == BOTTOM_LEFT_CORNER:  # bottom-left
                    center = Point(
                        corner.x + params.corner_radius, corner.y + params.corner_radius
                    )
                    start_angle = ANGLE_PI
                    end_angle = ANGLE_THREE_HALF_PI
                elif i == BOTTOM_RIGHT_CORNER:  # bottom-right
                    center = Point(
                        corner.x - params.corner_radius, corner.y + params.corner_radius
                    )
                    start_angle = ANGLE_THREE_HALF_PI
                    end_angle = ANGLE_TWO_PI
                elif i == TOP_RIGHT_CORNER:  # top-right
                    center = Point(
                        corner.x - params.corner_radius, corner.y - params.corner_radius
                    )
                    start_angle = ANGLE_ZERO
                    end_angle = ANGLE_HALF_PI
                else:  # top-left (TOP_LEFT_CORNER)
                    center = Point(
                        corner.x + params.corner_radius, corner.y - params.corner_radius
                    )
                    start_angle = ANGLE_HALF_PI
                    end_angle = ANGLE_PI

                arc = Arc(
                    center=center,
                    radius=params.corner_radius,
                    start_angle=start_angle,
                    end_angle=end_angle,
                    width=params.track_width,
                )
                points = arc.to_points(params.segment_number)
                for j in range(len(points) - 1):
                    self.drawline(
                        x1=points[j].x,
                        y1=points[j].y,
                        x2=points[j + 1].x,
                        y2=points[j + 1].y,
                        line_width=params.track_width,
                        layer_index=layer_index,
                        net_number=params.net_number,
                    )

            # Draw connection tabs and vias if ports are enabled
            if params.port_gap > 0:
                # Draw horizontal connection tabs (like in draw_helix method)
                if turn != 0:  # Bottom tab (connects from previous layer)
                    self.drawline(
                        x1=params.x0 + params.width / HALF_DIVISOR,
                        y1=port_bottom_y,
                        x2=tab_x,
                        y2=port_bottom_y,  # Horizontal tab
                        line_width=params.connect_width,
                        layer_index=layer_index,
                        net_number=params.net_number,
                    )

                if (
                    turn != len(params.layer_index_list) - 1
                ):  # Top tab (connects to next layer)
                    self.drawline(
                        x1=params.x0 + params.width / HALF_DIVISOR,
                        y1=port_top_y,
                        x2=tab_x,
                        y2=port_top_y,  # Horizontal tab
                        line_width=params.connect_width,
                        layer_index=layer_index,
                        net_number=params.net_number,
                    )

                    # Add via to connect to next layer
                    next_layer = params.layer_index_list[turn + 1]
                    self.draw_via(
                        x=tab_x,
                        y=port_top_y,  # Via at horizontal tab end
                        via_size=params.via_size,
                        drill_size=params.drill_size,
                        net_number=params.net_number,
                        layer_index_1=layer_index,
                        layer_index_2=next_layer,
                    )
            else:
                # Original behavior: via at top-right corner
                if layer_index != params.layer_index_list[-1]:
                    next_layer = params.layer_index_list[
                        params.layer_index_list.index(layer_index) + 1
                    ]
                    self.draw_via(
                        x=corners[TOP_RIGHT_CORNER].x,
                        y=corners[TOP_RIGHT_CORNER].y,
                        via_size=params.via_size,
                        drill_size=params.drill_size,
                        net_number=params.net_number,
                        layer_index_1=layer_index,
                        layer_index_2=next_layer,
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

    def set_mode(self, mode: Literal["print", "file"]) -> None:
        """Switch between print and file modes.

        Args:
            mode: "print" for direct s-expression output, "file" for collecting elements

        """
        if mode != self.mode:
            self.mode = mode
            self.elements = []  # Always clear buffer when switching modes

    def save(self, output_path: str, template_path: str = "asset.kicad_pcb") -> None:
        """Save PCB elements to a KiCad PCB file using a template.

        This method only works when in file mode.
        """
        if self.mode != "file":
            print("Warning: Not in file mode. Use set_mode('file') first.")
            return

        try:
            with open(template_path, "r") as f:
                template_content = f.read()
        except FileNotFoundError:
            print(f"Template file {template_path} not found.")
            return

        # Find the last closing parenthesis of the file
        last_closing = template_content.rstrip().rfind(")")
        if last_closing == -1:
            print("Invalid template file format.")
            return

        # Insert our elements before the last closing parenthesis
        new_content = (
            template_content[:last_closing]
            + "\n"
            + "\n".join(self.elements)
            + "\n"
            + template_content[last_closing:]
        )

        # Write the modified content to the output file
        with open(output_path, "w") as f:
            f.write(new_content)

        print(f"PCB elements saved to {output_path}")

    def enable_visualization(self, width: float = 800, height: float = 600) -> None:
        """Enable SVG visualization.

        Args:
            width: SVG canvas width in pixels
            height: SVG canvas height in pixels
        """
        self.visualizer = PCBVisualizer(width, height)

    def save_svg(self, filename: str) -> None:
        """Save current visualization as SVG file.

        Args:
            filename: Output SVG filename
        """
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return
        self.visualizer.save_svg(filename)

    def get_svg(self) -> str:
        """Get SVG string of current visualization.

        Returns:
            SVG string, or empty string if visualization not enabled
        """
        if not self.visualizer:
            return ""
        return self.visualizer.generate_svg()

    def show_svg(self) -> None:
        """Display SVG in Jupyter notebook or print SVG string."""
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return

        svg_content = self.visualizer.generate_svg()

        # Try to display in Jupyter
        try:
            from IPython.display import SVG, display

            display(SVG(svg_content))
        except ImportError:
            # Not in Jupyter, print SVG
            print("SVG content (save to .svg file to view):")
            print(svg_content)

    def show_layer(self, layer: str) -> None:
        """Show a specific layer in visualization.

        Args:
            layer: Layer name (e.g., "F.Cu", "In1.Cu", "B.Cu")
        """
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return
        self.visualizer.show_layer(layer)

    def hide_layer(self, layer: str) -> None:
        """Hide a specific layer in visualization.

        Args:
            layer: Layer name (e.g., "F.Cu", "In1.Cu", "B.Cu")
        """
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return
        self.visualizer.hide_layer(layer)

    def toggle_layer(self, layer: str) -> bool:
        """Toggle layer visibility in visualization.

        Args:
            layer: Layer name (e.g., "F.Cu", "In1.Cu", "B.Cu")

        Returns:
            True if layer is now visible, False if hidden
        """
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return False
        return self.visualizer.toggle_layer(layer)

    def show_only_layer(self, layer: str) -> None:
        """Show only the specified layer, hide all others.

        Args:
            layer: Layer name to show exclusively
        """
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return
        self.visualizer.show_only_layer(layer)

    def show_all_layers(self) -> None:
        """Show all layers in visualization."""
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return
        self.visualizer.show_all_layers()

    def hide_all_layers(self) -> None:
        """Hide all layers in visualization."""
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return
        self.visualizer.hide_all_layers()

    def toggle_vias(self) -> bool:
        """Toggle via visibility in visualization.

        Returns:
            True if vias are now visible, False if hidden
        """
        if not self.visualizer:
            print("Visualization not enabled. Call enable_visualization() first.")
            return False
        return self.visualizer.toggle_vias()

    def get_available_layers(self) -> List[str]:
        """Get list of all layers that have elements.

        Returns:
            List of layer names, or empty list if visualization not enabled
        """
        if not self.visualizer:
            return []
        return self.visualizer.get_available_layers()

    def get_visible_layers(self) -> List[str]:
        """Get list of currently visible layers.

        Returns:
            List of visible layer names, or empty list if visualization not enabled
        """
        if not self.visualizer:
            return []
        return self.visualizer.get_visible_layers()

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
