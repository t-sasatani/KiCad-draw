"""KiCad output formatting."""

from typing import List

from kicad_draw.geometry import Line, Via


class KiCadFormatter:
    """Formats geometric primitives into KiCad PCB format."""

    def format_segment(self, line: Line, layer: str, net: int) -> str:
        """Format a line segment."""
        return (
            f"(segment (start {line.start.x} {line.start.y}) "
            f"(end {line.end.x} {line.end.y}) "
            f"(width {line.width}) "
            f'(layer "{layer}") '
            f"(net {net}) "
            f"(tstamp 0))"
        )

    def format_via(self, via: Via, layers: List[str], net: int) -> str:
        """Format a via."""
        return (
            f"(via (at {via.position.x} {via.position.y}) "
            f"(size {via.size}) "
            f"(drill {via.drill_size}) "
            f'(layers "{layers[0]}" "{layers[1]}") '
            f"(net {net}) "
            f"(tstamp 0))"
        )
