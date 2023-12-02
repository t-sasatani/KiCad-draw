### Documentation
https://kicad-draw.readthedocs.io/en/latest/

### Install
```
pip install kicad-draw
```

### How to use
Currently, manual edits to the .kicad_pcb file are required (Issue https://github.com/t-sasatani/KiCad-coil-maker/issues/1#issue-1837077917)
- Set coil parameters and generate design text using the code (see the below notebook for example).
- Open the .kicad_pcb file using a text editor
- Paste the generated design text before the last closing bracket `)`.

### Examples
[examples/kicad_helix_coil.ipynb
](https://github.com/t-sasatani/KiCad-coil-maker/blob/master/examples/kicad_helix_coil.ipynb)
<a href="https://colab.research.google.com/github/t-sasatani/KiCad-coil-maker/blob/master/examples/kicad_helix_coil.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
