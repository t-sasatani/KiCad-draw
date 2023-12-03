Usage
=====

.. _installation:

Installation
------------

To use kicad-draw, first install it using pip:

.. code-block:: console

   (.venv) $ pip install kicad-draw


How to use
------------

Currently, manual edits to the .kicad_pcb file are required (Issue https://github.com/t-sasatani/KiCad-coil-maker/issues/1#issue-1837077917)

* Generate design text using the code (see notebooks for example).

* Open the `.kicad_pcb` file using a text editor

* Paste the generated design text before the last closing bracket `)`.


Notebooks
------------

* https://github.com/t-sasatani/KiCad-draw/blob/master/examples/kicad_helix_coil.ipynb
