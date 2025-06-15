# Examples and Visualizations

This page showcases the capabilities of KiCad-draw with interactive SVG visualizations. All examples generate both KiCad-compatible s-expressions and SVG visualizations for preview.

## Circular Helix Coils

Circular helix coils are the classic spiral inductors commonly used in RF applications. They provide excellent Q-factor and are space-efficient for high-frequency designs.

### Multi-Layer Circular Helix

This example shows a 4-layer circular helix coil with proper via connections between layers:

```python
from kicad_draw.models import HelixParams
from kicad_draw.PCBmodule import PCBdraw

# Define parameters
params = HelixParams(
    x0=150.0,           # Center X coordinate (mm)
    y0=100.0,           # Center Y coordinate (mm)
    radius=11.0,        # Coil radius (mm)
    port_gap=0.65,      # Port opening size (mm)
    tab_gap=0.55,       # Tab extension distance (mm)
    angle_step=0.1,     # Angular step between layers (radians)
    layer_index_list=[0, 1, 2, 3],  # F.Cu, In1.Cu, In2.Cu, In3.Cu
    track_width=0.5,    # Main trace width (mm)
    connect_width=0.2,  # Connection trace width (mm)
    drill_size=0.2,     # Via drill diameter (mm)
    via_size=0.4,       # Via outer diameter (mm)
    net_number=1,       # KiCad net number
    segment_number=100, # Number of arc segments
)

# Generate the coil
pcb = PCBdraw(stackup="default_6layer", mode="file")
pcb.draw_helix(params)

# Visualize
svg_content = pcb.visualize(visible_layers=[0, 1, 2, 3], show_vias=True)
```

#### All Layers Visible
This visualization shows all 4 layers of the circular helix with different colors for each layer:

<img src="_static/images/circular_helix_all_layers.svg" alt="Circular Helix - All Layers" width="400"/>

#### Outer Layers Only
This shows only the front copper (F.Cu) and inner layer 3 (In3.Cu) to highlight the overall coil structure:

<img src="_static/images/circular_helix_outer_layers.svg" alt="Circular Helix - Outer Layers" width="400"/>

**Key Features:**
- **Consistent via spacing**: Vias are positioned with ~0.68mm spacing
- **Proper layer connections**: Each layer connects to the next via tabs and vias
- **Angular offset**: Each layer has a slight angular offset for optimal magnetic coupling

## Rectangular Helix Coils

Rectangular helix coils offer better space utilization in constrained layouts and can provide different inductance characteristics compared to circular coils.

### Multi-Layer Rectangular Helix

This example demonstrates a 4-layer rectangular helix with rounded corners and port connections:

```python
from kicad_draw.models import HelixRectangleParams
from kicad_draw.PCBmodule import PCBdraw

# Define parameters
params = HelixRectangleParams(
    x0=150.0,           # Center X coordinate (mm)
    y0=100.0,           # Center Y coordinate (mm)
    width=30.0,         # Rectangle width (mm)
    height=20.0,        # Rectangle height (mm)
    corner_radius=3.0,  # Corner rounding radius (mm)
    layer_index_list=[0, 1, 2, 3],  # F.Cu, In1.Cu, In2.Cu, In3.Cu
    track_width=0.5,    # Main trace width (mm)
    connect_width=0.3,  # Connection trace width (mm)
    drill_size=0.2,     # Via drill diameter (mm)
    via_size=0.4,       # Via outer diameter (mm)
    net_number=1,       # KiCad net number
    port_gap=0.65,      # Port opening size (mm)
    tab_gap=0.55,       # Tab extension distance (mm)
)

# Generate the coil
pcb = PCBdraw(stackup="default_6layer", mode="file")
pcb.draw_helix_rectangle(params)

# Visualize
svg_content = pcb.visualize(visible_layers=[0, 1, 2, 3], show_vias=True)
```

#### All Layers Visible
This visualization shows all 4 layers of the rectangular helix:

<img src="_static/images/rectangular_helix_all_layers.svg" alt="Rectangular Helix - All Layers" width="400"/>

#### Outer Layers Only
This shows the front copper and inner layer 3 to highlight the rectangular structure:

<img src="_static/images/rectangular_helix_outer_layers.svg" alt="Rectangular Helix - Outer Layers" width="400"/>

**Key Features:**
- **Consistent via spacing**: Now matches circular helix with ~0.65mm spacing (after our fix!)
- **Proper tab alignment**: Bottom tab of each layer connects to top tab of previous layer
- **Rounded corners**: Smooth transitions reduce current concentration
- **Port connections**: Tabs extend horizontally for easy external connections

## Side-by-Side Comparison

This example shows both circular and rectangular coils in the same design for direct comparison:

<img src="_static/images/comparison_circular_vs_rectangular.svg" alt="Circular vs Rectangular Comparison" width="600"/>

**Comparison Highlights:**
- **Size efficiency**: Rectangular coils can fit better in constrained spaces
- **Via spacing**: Both now have consistent spacing (~0.65mm)
- **Connection style**: Different tab orientations for different layout requirements
- **Magnetic coupling**: Different field patterns for different applications

## Layer Legend

The visualizations use the following color scheme:
- **Red**: F.Cu (Front Copper, Layer 0)
- **Blue**: In1.Cu (Inner Layer 1)
- **Green**: In2.Cu (Inner Layer 2)  
- **Orange**: In3.Cu (Inner Layer 3)
- **Purple**: B.Cu (Back Copper, Layer 5)
- **Black circles**: Vias with drill holes

## Export Options

All examples can be exported in multiple formats:

### KiCad S-Expressions
```python
# Export for direct paste into .kicad_pcb files
s_expressions = pcb.export()
print(s_expressions)
```

### SVG Visualization
```python
# Generate interactive SVG
svg_content = pcb.visualize(
    visible_layers=[0, 1, 2, 3],  # Choose which layers to show
    show_vias=True,               # Show/hide vias
    width=800,                    # SVG width in pixels
    height=600                    # SVG height in pixels
)
```

### File Output
```python
# Save to KiCad PCB file
pcb.save("my_coil_design.kicad_pcb")

# Save SVG to file
with open("my_coil_visualization.svg", "w") as f:
    f.write(svg_content)
```

## Design Guidelines

### Via Spacing Optimization
- Both circular and rectangular helix functions now use consistent via spacing
- Spacing is primarily controlled by the `port_gap` parameter
- Smaller `port_gap` values create tighter coil windings

### Layer Selection
- Use consecutive layers for best magnetic coupling
- Consider stackup impedance when choosing layers
- More layers = higher inductance but also higher resistance

### Geometric Parameters
- **Circular**: Optimize `radius` and `angle_step` for desired inductance
- **Rectangular**: Adjust `width`, `height`, and `corner_radius` for space constraints
- **Both**: Match `track_width` to your PCB design rules

## Troubleshooting

### Common Issues
1. **Vias not aligning**: Fixed in recent updates - tabs now properly align between layers
2. **Inconsistent spacing**: Fixed - both coil types now use the same spacing algorithm
3. **Overlapping traces**: Increase `port_gap` or adjust layer count

### Verification
Always verify your generated coils by:
1. Checking the SVG visualization
2. Running DRC in KiCad after importing
3. Confirming via connections in 3D view

---

*These examples demonstrate the latest improvements to KiCad-draw, including the tab alignment fix and via spacing consistency improvements.* 