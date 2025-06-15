Usage
=====

.. _installation:

Installation
------------

To use kicad-draw, first install it using pip:

.. code-block:: console

   (.venv) $ pip install kicad-draw


Basic Usage
-----------

kicad-draw provides a Python API for generating PCB coil patterns. Here's a simple example:

.. code-block:: python

   from kicad_draw import PCBdraw
   from kicad_draw.models import HelixParams

   # Create a PCB instance
   pcb = PCBdraw("default_4layer")

   # Define helix parameters
   params = HelixParams(
       x0=50.0, y0=50.0,  # Center position (mm)
       radius=10.0,       # Coil radius (mm)
       port_gap=2.0,      # Gap for ports (mm)
       tab_gap=1.0,       # Connection tab extension (mm)
       angle_step=0.5,    # Angular step between layers (radians)
       layer_index_list=[0, 1],  # Use F.Cu and In1.Cu layers
       track_width=0.2,   # Track width (mm)
       connect_width=0.1, # Connection width (mm)
       drill_size=0.2,    # Via drill size (mm)
       via_size=0.4,      # Via outer size (mm)
       net_number=1       # KiCad net number
   )

   # Draw the helix coil
   pcb.draw_helix(params)

   # Export as KiCad s-expressions
   output = pcb.export()
   print(output)


Parameter Configuration
-----------------------

**Helix Coil Parameters**

The `HelixParams` class defines all parameters for circular coils:

- **Position**: `x0`, `y0` - Center coordinates in mm
- **Geometry**: `radius` - Coil radius in mm
- **Gaps**: `port_gap`, `tab_gap` - Port and connection gaps in mm
- **Layers**: `layer_index_list` - List of copper layer indices (0=F.Cu, 1=In1.Cu, etc.)
- **Traces**: `track_width`, `connect_width` - Trace widths in mm
- **Vias**: `drill_size`, `via_size` - Via dimensions in mm
- **Electrical**: `net_number` - KiCad net number for connectivity

**Rectangular Coil Parameters**

The `HelixRectangleParams` class defines parameters for rectangular coils:

- **Position**: `x0`, `y0` - Center coordinates in mm
- **Geometry**: `width`, `height`, `corner_radius` - Rectangle dimensions in mm
- **Other parameters**: Same as HelixParams


Visualization
-------------

kicad-draw includes SVG visualization capabilities:

.. code-block:: python

   # Enable visualization (default)
   pcb = PCBdraw("default_4layer", enable_visualization=True)

   # Draw your coil
   pcb.draw_helix(params)

   # Show SVG visualization
   pcb.show_svg()

   # Control layer visibility
   pcb.hide_layer("F.Cu")
   pcb.show_only_layer("In1.Cu")
   pcb.toggle_layer("B.Cu")

   # Save visualization
   pcb.save_svg("my_coil.svg")


File Integration
----------------

Currently, manual edits to the .kicad_pcb file are required (Issue https://github.com/t-sasatani/KiCad-coil-maker/issues/1#issue-1837077917)

1. Generate design text using the code (see notebooks for example).
2. Open the `.kicad_pcb` file using a text editor
3. Paste the generated design text before the last closing bracket `)`.


Command Line Interface
----------------------

kicad-draw provides a basic CLI:

.. code-block:: console

   $ kicad-draw version
   kicad-draw version 1.0.0


Examples
--------

**Notebooks**

* `Helix Coil Example <https://github.com/t-sasatani/KiCad-draw/blob/master/examples/kicad_helix_coil.ipynb>`_
* `Rectangular Helix Coil Example <https://github.com/t-sasatani/KiCad-draw/blob/master/examples/kicad_helix_rect_coil.ipynb>`_

**Google Colab**

* `Open Helix Coil in Colab <https://colab.research.google.com/github/t-sasatani/KiCad-coil-maker/blob/master/examples/kicad_helix_coil.ipynb>`_


Troubleshooting
---------------

**Common Issues**

* **Invalid layer index**: Ensure layer indices match your PCB stackup (0=F.Cu, 1=In1.Cu, etc.)
* **Via size too small**: Ensure `via_size` > `drill_size`
* **Visualization not showing**: Check that `enable_visualization=True` and layers are visible
* **Export empty**: Ensure you've drawn elements before calling `export()`
