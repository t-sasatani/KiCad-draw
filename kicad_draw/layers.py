"""Layer management for PCB drawing."""

from typing import List, Literal

from kicad_draw.config import default_layers


class LayerManager:
    """Manages PCB layers and stackups."""

    def __init__(self, stackup: Literal[tuple(default_layers)]):
        """Initialize with a specific stackup."""
        self.layers = default_layers[stackup]["layer_list"]

    def validate_layer(self, index: int) -> bool:
        """Check if layer index is valid."""
        return 0 <= index < len(self.layers)

    def get_layer_name(self, index: int) -> str:
        """Get layer name by index."""
        if not self.validate_layer(index):
            raise ValueError(f"Invalid layer index: {index}")
        return self.layers[index]

    def validate_layers(self, indices: List[int]) -> bool:
        """Check if all layer indices are valid."""
        return all(self.validate_layer(index) for index in indices)

    def get_layer_names(self, indices: List[int]) -> List[str]:
        """Get layer names by indices."""
        if not self.validate_layers(indices):
            raise ValueError(f"Invalid layer indices: {indices}")
        return [self.layers[index] for index in indices]
