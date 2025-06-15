"""SVG-based visualization for PCB patterns."""

import math
from typing import List, Optional, Tuple
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from .config import default_layers
from .geometry import Point


class PCBVisualizer:
    """SVG-based visualizer for PCB patterns."""

    # Layer colors (professional PCB color scheme)
    LAYER_COLORS = {
        "F.Cu": "#C8860D",  # Top copper (gold)
        "In1.Cu": "#CC0000",  # Inner layer 1 (red)
        "In2.Cu": "#00CC00",  # Inner layer 2 (green)
        "In3.Cu": "#0000CC",  # Inner layer 3 (blue)
        "In4.Cu": "#CC00CC",  # Inner layer 4 (magenta)
        "B.Cu": "#008080",  # Bottom copper (teal)
    }

    VIA_COLOR = "#404040"  # Dark gray for vias
    BACKGROUND_COLOR = "#1a1a1a"  # Dark PCB substrate

    def __init__(self, width: float = 800, height: float = 600):
        """Initialize SVG visualizer.

        Args:
            width: SVG canvas width in pixels
            height: SVG canvas height in pixels
        """
        self.width = width
        self.height = height
        self.elements = []
        self.bounds = None  # Will be calculated from elements

    def add_line(
        self, x1: float, y1: float, x2: float, y2: float, width: float, layer: str
    ) -> None:
        """Add a line element."""
        self.elements.append(
            {
                "type": "line",
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "width": width,
                "layer": layer,
            }
        )
        self._update_bounds(x1, y1)
        self._update_bounds(x2, y2)

    def add_via(self, x: float, y: float, size: float) -> None:
        """Add a via element."""
        self.elements.append({"type": "via", "x": x, "y": y, "size": size})
        self._update_bounds(x - size / 2, y - size / 2)
        self._update_bounds(x + size / 2, y + size / 2)

    def add_arc(
        self,
        center_x: float,
        center_y: float,
        radius: float,
        start_angle: float,
        end_angle: float,
        width: float,
        layer: str,
        segments: int = 32,
    ) -> None:
        """Add an arc by converting to line segments."""
        angle_step = (end_angle - start_angle) / segments

        for i in range(segments):
            angle1 = start_angle + i * angle_step
            angle2 = start_angle + (i + 1) * angle_step

            x1 = center_x + radius * math.cos(angle1)
            y1 = center_y + radius * math.sin(angle1)
            x2 = center_x + radius * math.cos(angle2)
            y2 = center_y + radius * math.sin(angle2)

            self.add_line(x1, y1, x2, y2, width, layer)

    def _update_bounds(self, x: float, y: float) -> None:
        """Update the bounding box of all elements."""
        if self.bounds is None:
            self.bounds = [x, y, x, y]  # [min_x, min_y, max_x, max_y]
        else:
            self.bounds[0] = min(self.bounds[0], x)
            self.bounds[1] = min(self.bounds[1], y)
            self.bounds[2] = max(self.bounds[2], x)
            self.bounds[3] = max(self.bounds[3], y)

    def _calculate_transform(self) -> Tuple[float, float, float]:
        """Calculate transform to fit content in canvas with margin."""
        if not self.bounds:
            return 1.0, 0.0, 0.0

        margin = 50  # pixels
        content_width = self.bounds[2] - self.bounds[0]
        content_height = self.bounds[3] - self.bounds[1]

        if content_width == 0 or content_height == 0:
            return 1.0, 0.0, 0.0

        # Calculate scale to fit with margin
        scale_x = (self.width - 2 * margin) / content_width
        scale_y = (self.height - 2 * margin) / content_height
        scale = min(scale_x, scale_y)

        # Calculate translation to center content
        translate_x = (
            margin - self.bounds[0] * scale + (self.width - content_width * scale) / 2
        )
        translate_y = (
            margin - self.bounds[1] * scale + (self.height - content_height * scale) / 2
        )

        return scale, translate_x, translate_y

    def generate_svg(self) -> str:
        """Generate SVG string."""
        if not self.elements:
            return self._empty_svg()

        scale, translate_x, translate_y = self._calculate_transform()

        # Create SVG root
        svg = Element("svg")
        svg.set("width", str(self.width))
        svg.set("height", str(self.height))
        svg.set("xmlns", "http://www.w3.org/2000/svg")
        svg.set("viewBox", f"0 0 {self.width} {self.height}")

        # Add background
        bg = SubElement(svg, "rect")
        bg.set("width", "100%")
        bg.set("height", "100%")
        bg.set("fill", self.BACKGROUND_COLOR)

        # Create main group with transform
        main_group = SubElement(svg, "g")
        main_group.set(
            "transform", f"translate({translate_x},{translate_y}) scale({scale})"
        )

        # Group elements by layer for proper rendering order
        layers = {}
        vias = []

        for element in self.elements:
            if element["type"] == "via":
                vias.append(element)
            else:
                layer = element["layer"]
                if layer not in layers:
                    layers[layer] = []
                layers[layer].append(element)

        # Render layers (bottom to top)
        layer_order = ["B.Cu", "In4.Cu", "In3.Cu", "In2.Cu", "In1.Cu", "F.Cu"]
        for layer_name in layer_order:
            if layer_name in layers:
                layer_group = SubElement(main_group, "g")
                layer_group.set("class", f'layer-{layer_name.replace(".", "-")}')

                color = self.LAYER_COLORS.get(layer_name, "#888888")

                for element in layers[layer_name]:
                    if element["type"] == "line":
                        line = SubElement(layer_group, "line")
                        line.set("x1", str(element["x1"]))
                        line.set("y1", str(element["y1"]))
                        line.set("x2", str(element["x2"]))
                        line.set("y2", str(element["y2"]))
                        line.set("stroke", color)
                        line.set("stroke-width", str(element["width"]))
                        line.set("stroke-linecap", "round")

        # Render vias on top
        if vias:
            via_group = SubElement(main_group, "g")
            via_group.set("class", "vias")

            for via in vias:
                circle = SubElement(via_group, "circle")
                circle.set("cx", str(via["x"]))
                circle.set("cy", str(via["y"]))
                circle.set("r", str(via["size"] / 2))
                circle.set("fill", self.VIA_COLOR)
                circle.set("stroke", "#666666")
                circle.set("stroke-width", "0.1")

        # Add legend
        self._add_legend(svg, layers.keys())

        # Convert to string with pretty formatting
        rough_string = tostring(svg, "unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def _add_legend(self, svg: Element, used_layers: List[str]) -> None:
        """Add a legend showing layer colors."""
        if not used_layers:
            return

        legend_group = SubElement(svg, "g")
        legend_group.set("class", "legend")

        legend_x = 20
        legend_y = 30

        # Legend background
        legend_bg = SubElement(legend_group, "rect")
        legend_bg.set("x", str(legend_x - 10))
        legend_bg.set("y", str(legend_y - 20))
        legend_bg.set("width", str(120))
        legend_bg.set("height", str(len(used_layers) * 25 + 30))
        legend_bg.set("fill", "rgba(0,0,0,0.8)")
        legend_bg.set("stroke", "#666")
        legend_bg.set("rx", "5")

        # Legend title
        title = SubElement(legend_group, "text")
        title.set("x", str(legend_x))
        title.set("y", str(legend_y))
        title.set("fill", "white")
        title.set("font-family", "Arial, sans-serif")
        title.set("font-size", "14")
        title.set("font-weight", "bold")
        title.text = "Layers"

        # Layer entries
        for i, layer in enumerate(sorted(used_layers)):
            y_pos = legend_y + 25 + i * 20

            # Color swatch
            swatch = SubElement(legend_group, "rect")
            swatch.set("x", str(legend_x))
            swatch.set("y", str(y_pos - 8))
            swatch.set("width", "16")
            swatch.set("height", "12")
            swatch.set("fill", self.LAYER_COLORS.get(layer, "#888888"))

            # Layer name
            text = SubElement(legend_group, "text")
            text.set("x", str(legend_x + 25))
            text.set("y", str(y_pos))
            text.set("fill", "white")
            text.set("font-family", "Arial, sans-serif")
            text.set("font-size", "12")
            text.text = layer

    def _empty_svg(self) -> str:
        """Generate empty SVG with message."""
        svg = Element("svg")
        svg.set("width", str(self.width))
        svg.set("height", str(self.height))
        svg.set("xmlns", "http://www.w3.org/2000/svg")

        # Background
        bg = SubElement(svg, "rect")
        bg.set("width", "100%")
        bg.set("height", "100%")
        bg.set("fill", self.BACKGROUND_COLOR)

        # Message
        text = SubElement(svg, "text")
        text.set("x", str(self.width // 2))
        text.set("y", str(self.height // 2))
        text.set("text-anchor", "middle")
        text.set("fill", "white")
        text.set("font-family", "Arial, sans-serif")
        text.set("font-size", "18")
        text.text = "No PCB elements to display"

        rough_string = tostring(svg, "unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def save_svg(self, filename: str) -> None:
        """Save SVG to file."""
        with open(filename, "w") as f:
            f.write(self.generate_svg())
        print(f"SVG saved to {filename}")

    def clear(self) -> None:
        """Clear all elements."""
        self.elements = []
        self.bounds = None
