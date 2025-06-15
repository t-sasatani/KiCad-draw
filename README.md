# KiCad-draw

[![Tests](https://github.com/t-sasatani/KiCad-draw/actions/workflows/pytest.yml/badge.svg)](https://github.com/t-sasatani/KiCad-draw/actions/workflows/pytest.yml)
[![Documentation](https://github.com/t-sasatani/KiCad-draw/actions/workflows/docs.yml/badge.svg)](https://github.com/t-sasatani/KiCad-draw/actions/workflows/docs.yml)
[![PyPI version](https://badge.fury.io/py/kicad-draw.svg)](https://badge.fury.io/py/kicad-draw)
[![Python Support](https://img.shields.io/pypi/pyversions/kicad-draw.svg)](https://pypi.org/project/kicad-draw/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

A Python library for generating PCB coil patterns compatible with KiCad.

## 🚀 Features

- **Circular and rectangular helix coils** with customizable parameters
- **Multi-layer support** with proper via connections between layers  
- **KiCad-compatible output** (s-expression format)
- **SVG visualization** for design preview and verification
- **Consistent via spacing** and proper tab alignment (v0.4.0+ fixes)
- **Professional documentation** with interactive examples

## 📚 Documentation

**[📖 Full Documentation with Examples →](https://t-sasatani.github.io/KiCad-draw/)**

- [🚀 Quick Start Guide](https://t-sasatani.github.io/KiCad-draw/quickstart.html)
- [🎨 Examples with SVG Visualizations](https://t-sasatani.github.io/KiCad-draw/examples.html)
- [📘 API Reference](https://t-sasatani.github.io/KiCad-draw/api.html)
- [🔧 Development Guide](https://t-sasatani.github.io/KiCad-draw/dev.html)

## 📦 Installation

```bash
pip install kicad-draw
```

## ⚡ Quick Example

```python
from kicad_draw.models import HelixParams
from kicad_draw.PCBmodule import PCBdraw

# Define coil parameters
params = HelixParams(
    x0=150.0, y0=100.0,           # Center position (mm)
    radius=11.0,                  # Coil radius (mm)
    layer_index_list=[0, 1, 2, 3], # Use 4 layers
    track_width=0.5,              # Trace width (mm)
    port_gap=0.65,                # Via spacing control
)

# Generate the coil
pcb = PCBdraw(stackup="default_6layer")
pcb.draw_helix(params)

# Export for KiCad
kicad_output = pcb.export()

# Generate SVG visualization  
svg_preview = pcb.visualize(visible_layers=[0, 1, 2, 3], show_vias=True)
```

## 🎯 Recent Improvements (v0.4.1)

- **✅ Fixed critical tab alignment** - proper via connections between layers
- **✅ Consistent via spacing** - both circular and rectangular coils now use same algorithm
- **✅ Comprehensive documentation** - with SVG visualizations and examples
- **✅ Automated publishing** - GitHub Actions with PyPI trusted publishers
- **✅ 100% test coverage** - all 13 tests passing

## 🛠️ Supported Coil Types

| Coil Type | Parameters | Best For |
|-----------|------------|----------|
| **Circular Helix** | `HelixParams` | RF inductors, classic spiral coils |
| **Rectangular Helix** | `HelixRectangleParams` | Space-constrained layouts, different inductance profiles |

## 🎨 Visualization Examples

The library generates both KiCad-compatible files and SVG previews:

- **Multi-layer coils** with different colors per layer
- **Via connections** clearly visible
- **Interactive examples** in the documentation

[**→ See Visual Examples**](https://t-sasatani.github.io/KiCad-draw/examples.html)

## 🧪 Development Status

![Tests](https://img.shields.io/badge/tests-13%2F13%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)

## 📄 License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please see our [Development Guide](https://t-sasatani.github.io/KiCad-draw/dev.html) for details on setting up the development environment and running tests.

## 📈 Version History

- **v0.4.1** (Latest) - Infrastructure improvements, automated publishing
- **v0.4.0** - Critical bug fixes, enhanced documentation, SVG visualizations  
- **v0.3.0** - Rectangular helix support
- **v0.2.0** - SVG visualization, multi-layer support
- **v0.1.0** - Initial release with circular helix coils

[**→ Full Changelog**](https://t-sasatani.github.io/KiCad-draw/changelog.html)
