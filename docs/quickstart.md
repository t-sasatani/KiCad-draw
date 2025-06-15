# Quick Start Guide

Get started with KiCad-draw in just a few minutes! This guide shows you how to create your first PCB coil with visualization.

## Installation

```bash
pip install kicad-draw
```

## Your First Coil in 3 Steps

### Step 1: Import and Define Parameters

```python
from kicad_draw.models import HelixParams
from kicad_draw.PCBmodule import PCBdraw

# Create a simple 2-layer circular coil
params = HelixParams(
    x0=100.0,           # Center X (mm)
    y0=100.0,           # Center Y (mm)  
    radius=10.0,        # Radius (mm)
    port_gap=0.5,       # Port opening (mm)
    tab_gap=0.4,        # Tab extension (mm)
    angle_step=0.0,     # No angular offset
    layer_index_list=[0, 1],  # F.Cu and In1.Cu
    track_width=0.5,    # Track width (mm)
    connect_width=0.2,  # Connection width (mm)
    drill_size=0.2,     # Via drill (mm)
    via_size=0.4,       # Via size (mm)
    net_number=1        # KiCad net number
)
```

### Step 2: Generate the Coil

```python
# Create PCB instance
pcb = PCBdraw(stackup="default_4layer", mode="file")

# Draw the coil
pcb.draw_helix(params)

# Generate visualization
svg = pcb.visualize(visible_layers=[0, 1], show_vias=True)
```

### Step 3: Export Your Results

```python
# Export KiCad s-expressions
kicad_code = pcb.export()
print("Copy this into your .kicad_pcb file:")
print(kicad_code)

# Save visualization
with open("my_coil.svg", "w") as f:
    f.write(svg)
```

## What You Get

- **KiCad-compatible s-expressions** that you can directly paste into your PCB file
- **SVG visualization** for immediate preview and documentation
- **Proper via connections** between layers
- **Consistent spacing** and alignment

## Next Steps

- Explore the [Examples](examples.md) page for more complex designs
- Check the [API Reference](api.rst) for all available parameters
- Learn about rectangular coils in the examples for space-constrained designs

## Common Parameters Explained

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `radius` | Coil radius for circular designs | 5-20 mm |
| `width/height` | Rectangle dimensions | 10-50 mm |
| `track_width` | Main trace width | 0.1-1.0 mm |
| `port_gap` | Opening between coil turns | 0.2-2.0 mm |
| `layer_index_list` | Which PCB layers to use | [0,1] to [0,1,2,3,4,5] |
| `via_size` | Via outer diameter | 0.4-0.8 mm |

## Tips for Success

1. **Start simple**: Begin with 2-layer designs before adding more layers
2. **Check constraints**: Ensure via sizes match your PCB manufacturer's capabilities  
3. **Visualize first**: Always check the SVG before importing to KiCad
4. **Test in KiCad**: Run DRC after importing to catch any issues

---

Ready to create more complex designs? Head to the [Examples](examples.md) page to see advanced multi-layer coils with full visualizations! 