Usage
=====

Installation
------------

To use kicad-draw, first install it using pip:

.. code-block:: console

   pip install kicad-draw

Basic Example
-------------

.. code-block:: python

   from kicad_draw import PCBdraw
   from kicad_draw.models import HelixParams

   # Create PCB and define parameters
   pcb = PCBdraw("default_4layer")
   params = HelixParams(
       x0=50.0, y0=50.0, radius=10.0, port_gap=2.0, tab_gap=1.0,
       angle_step=0.5, layer_index_list=[0, 1], track_width=0.2,
       connect_width=0.1, drill_size=0.2, via_size=0.4, net_number=1
   )

   # Generate and export
   pcb.draw_helix(params)
   output = pcb.export()

Examples
--------

See the example notebooks in the `examples/` directory for detailed usage patterns.
