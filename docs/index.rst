.. KiCad-draw documentation master file, created by
   sphinx-quickstart on Sat Dec  2 17:30:44 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

KiCad-draw documentation
======================================

A Python library for generating PCB coil patterns compatible with KiCad. Create circular and rectangular helix coils with precise control over geometry, layers, and electrical properties.

Contents
--------
.. toctree::
   :maxdepth: 2

   usage
   tutorial
   api
   dev

Features
--------
- Generate circular and rectangular helix coil patterns
- Multi-layer PCB support (4-layer and 6-layer stackups)
- SVG visualization with layer control
- Export to KiCad PCB format (s-expressions)
- Type-safe parameter validation using Pydantic
- Interactive Jupyter notebook examples

Quick Start
-----------

Install kicad-draw:

.. code-block:: console

   pip install kicad-draw

Create a simple helix coil:

.. code-block:: python

   from kicad_draw import PCBdraw
   from kicad_draw.models import HelixParams

   # Create PCB instance
   pcb = PCBdraw("default_4layer")

   # Define coil parameters
   params = HelixParams(
       x0=50.0, y0=50.0, radius=10.0,
       port_gap=2.0, tab_gap=1.0, 
       angle_step=0.5, layer_index_list=[0, 1],
       track_width=0.2, connect_width=0.1,
       drill_size=0.2, via_size=0.4, net_number=1
   )

   # Generate coil and export
   pcb.draw_helix(params)
   output = pcb.export()

Contributes
------------

- Issue Tracker: https://github.com/t-sasatani/KiCad-draw/issues
- Source Code: https://github.com/t-sasatani/KiCad-draw

License
------------

The project is licensed under AGPL-3.0 license.