Tutorial
========

This tutorial will guide you through creating various types of PCB coil patterns using kicad-draw.

Getting Started
---------------

**Prerequisites**

- Python 3.10 or higher
- Basic understanding of PCB layer stackups
- KiCad (for importing generated files)

**Installation**

.. code-block:: console

   pip install kicad-draw

**Import the necessary modules**

.. code-block:: python

   from kicad_draw import PCBdraw
   from kicad_draw.models import HelixParams, HelixRectangleParams

Creating Your First Coil
-------------------------

**Step 1: Initialize PCB**

.. code-block:: python

   # Create a 4-layer PCB instance
   pcb = PCBdraw("default_4layer")

   # For 6-layer PCB, use:
   # pcb = PCBdraw("default_6layer")

**Step 2: Define Coil Parameters**

.. code-block:: python

   params = HelixParams(
       x0=25.0,          # X-center position (mm)
       y0=25.0,          # Y-center position (mm)
       radius=8.0,       # Coil radius (mm)
       port_gap=1.5,     # Gap for ports (mm)
       tab_gap=2.0,      # Connection tab extension (mm)
       angle_step=0.8,   # Angular step between layers (radians)
       layer_index_list=[0, 1, 2, 3],  # F.Cu, In1.Cu, In2.Cu, In3.Cu
       track_width=0.15, # Main track width (mm)
       connect_width=0.1, # Via connection width (mm)
       drill_size=0.15,  # Via drill diameter (mm)
       via_size=0.35,    # Via outer diameter (mm)
       net_number=1      # KiCad net number
   )

**Step 3: Generate and Export**

.. code-block:: python

   # Draw the helix coil
   pcb.draw_helix(params)

   # Export as KiCad s-expressions
   kicad_data = pcb.export()
   
   # Save to file
   with open("my_coil.kicad_pcb_snippet", "w") as f:
       f.write(kicad_data)

Advanced Coil Patterns
----------------------

**Multi-Layer Spiral Coil**

.. code-block:: python

   params = HelixParams(
       x0=30.0, y0=30.0,
       radius=12.0,
       port_gap=2.0,
       tab_gap=1.5,
       angle_step=1.57,  # π/2 radians (90 degrees)
       layer_index_list=[0, 1, 2, 3],  # All 4 layers
       track_width=0.2,
       connect_width=0.15,
       drill_size=0.2,
       via_size=0.4,
       net_number=2,
       tab_position="OUT",  # or "IN"
       base_angle_offset=0.785  # π/4 radians (45 degrees)
   )
   
   pcb.draw_helix(params)

**Rectangular Coil**

.. code-block:: python

   rect_params = HelixRectangleParams(
       x0=40.0, y0=40.0,      # Center position
       width=20.0,            # Rectangle width (mm)
       height=15.0,           # Rectangle height (mm)
       corner_radius=2.0,     # Rounded corner radius (mm)
       layer_index_list=[0, 1], # F.Cu and In1.Cu
       track_width=0.2,
       connect_width=0.15,
       drill_size=0.2,
       via_size=0.4,
       net_number=3,
       port_gap=1.0,          # Creates ports if > 0
       tab_gap=1.5
   )
   
   pcb.draw_helix_rectangle(rect_params)

Working with Visualization
--------------------------

**Enable Visualization**

.. code-block:: python

   # Create PCB with visualization enabled (default)
   pcb = PCBdraw("default_4layer", enable_visualization=True)

   # Or enable later with custom canvas size
   pcb.enable_visualization(width=1000, height=800)

**Layer Control**

.. code-block:: python

   # Draw your coil first
   pcb.draw_helix(params)

   # Show only specific layers
   pcb.show_only_layer("F.Cu")
   pcb.show_svg()  # Display in Jupyter

   # Toggle layer visibility
   pcb.toggle_layer("In1.Cu")
   
   # Show/hide all layers
   pcb.show_all_layers()
   pcb.hide_all_layers()

   # Control via visibility
   pcb.set_via_visibility(False)  # Hide vias
   pcb.toggle_vias()              # Toggle vias

**Save Visualizations**

.. code-block:: python

   # Save SVG file
   pcb.save_svg("my_coil_visualization.svg")

   # Get SVG as string
   svg_content = pcb.get_svg()

Layer Management
----------------

**Understanding Layer Indices**

.. code-block:: python

   # 4-layer stackup
   layer_mapping_4l = {
       0: "F.Cu",    # Front copper
       1: "In1.Cu",  # Inner layer 1
       2: "In2.Cu",  # Inner layer 2  
       3: "B.Cu"     # Back copper
   }

   # 6-layer stackup
   layer_mapping_6l = {
       0: "F.Cu",    # Front copper
       1: "In1.Cu",  # Inner layer 1
       2: "In2.Cu",  # Inner layer 2
       3: "In3.Cu",  # Inner layer 3
       4: "In4.Cu",  # Inner layer 4
       5: "B.Cu"     # Back copper
   }

**Check Available Layers**

.. code-block:: python

   # Get available layers in your design
   available = pcb.get_available_layers()
   print("Available layers:", available)

   # Get currently visible layers
   visible = pcb.get_visible_layers()
   print("Visible layers:", visible)

Integration with KiCad
----------------------

**Manual Integration (Current Method)**

1. Generate the coil pattern:

.. code-block:: python

   pcb = PCBdraw("default_4layer")
   pcb.draw_helix(params)
   output = pcb.export()

2. Open your `.kicad_pcb` file in a text editor

3. Locate the final closing parenthesis ``)`` at the end of the file

4. Paste the generated output just before this closing parenthesis

5. Save and open in KiCad

**Tips for Integration**

- Always backup your `.kicad_pcb` file before manual editing
- Use unique net numbers to avoid conflicts
- Verify via sizes match your PCB stackup requirements
- Check design rules after importing

Optimization and Best Practices
-------------------------------

**Performance Optimization**

.. code-block:: python

   # Disable visualization for large designs to save memory
   pcb = PCBdraw("default_4layer", enable_visualization=False)
   
   # Or disable it later
   pcb.disable_visualization()

   # Reduce segment count for simpler curves (default: 100)
   params.segment_number = 50  # Fewer segments = faster generation

**Design Guidelines**

- **Via Sizing**: Ensure `via_size` > `drill_size` (typically 2x drill size)
- **Track Width**: Follow your PCB manufacturer's minimum track width rules
- **Layer Spacing**: Consider your PCB stackup when setting `angle_step`
- **Port Gaps**: Make gaps large enough for external connections
- **Net Numbers**: Use unique net numbers for each coil to avoid shorts

**Common Parameter Ranges**

.. code-block:: python

   # Typical parameter ranges for 4-layer PCB
   typical_params = {
       'track_width': 0.1,      # 0.1-0.5mm (check fab limits)
       'connect_width': 0.1,    # 0.1-0.3mm
       'drill_size': 0.15,      # 0.15-0.4mm (check fab limits)
       'via_size': 0.35,        # 0.35-0.8mm
       'port_gap': '1.0-3.0',   # 1-3mm depending on connector
       'tab_gap': '1.0-2.0',    # 1-2mm for easy connections
       'angle_step': '0.5-1.57' # π/2 radians max for good spacing
   }

Troubleshooting
---------------

**Common Issues and Solutions**

1. **"Invalid layer index" error**
   
   - Check that layer indices match your PCB stackup
   - 4-layer: use indices 0-3
   - 6-layer: use indices 0-5

2. **Vias not connecting properly**
   
   - Ensure `via_size` > `drill_size`
   - Check that via placement doesn't conflict with tracks

3. **Visualization not showing**
   
   - Verify `enable_visualization=True`
   - Check that layers are visible using `get_visible_layers()`

4. **KiCad import errors**
   
   - Validate your `.kicad_pcb` file syntax
   - Ensure net numbers don't conflict with existing nets
   - Check that all parentheses are properly balanced

Next Steps
----------

- Explore the :doc:`api` reference for advanced features
- Check out the example notebooks for real-world usage patterns
- Visit the GitHub repository for the latest updates and community discussions 