# KiCad-draw Documentation

This directory contains the Sphinx documentation for KiCad-draw, including examples with SVG visualizations.

## Building the Documentation

### Prerequisites
```bash
# Install documentation dependencies
pip install sphinx sphinx_rtd_theme myst-parser
```

### Generate Examples (if needed)
```bash
cd docs
python generate_examples.py
```

This creates SVG visualizations in `_static/images/` used by the documentation.

### Build HTML Documentation
```bash
make html
```

The built documentation will be in `_build/html/`. Open `_build/html/index.html` in your browser to view.

### Clean Build (if needed)
```bash
make clean
make html
```

## Documentation Structure

- `index.rst` - Main documentation index
- `quickstart.md` - Quick start guide with basic examples
- `examples.md` - Comprehensive examples with SVG visualizations  
- `usage.rst` - Usage documentation
- `api.rst` - API reference
- `dev.md` - Development guide
- `generate_examples.py` - Script to generate SVG examples
- `_static/images/` - Generated SVG files for documentation

## Adding New Examples

1. **Update `generate_examples.py`** - Add new functions to generate SVG examples
2. **Run the generator** - `python generate_examples.py`  
3. **Update `examples.md`** - Add documentation and reference the new SVG files
4. **Rebuild docs** - `make html`

## Example SVG Files Generated

- `circular_helix_all_layers.svg` - 4-layer circular helix, all layers visible
- `circular_helix_outer_layers.svg` - Circular helix, outer layers only
- `rectangular_helix_all_layers.svg` - 4-layer rectangular helix, all layers visible
- `rectangular_helix_outer_layers.svg` - Rectangular helix, outer layers only
- `comparison_circular_vs_rectangular.svg` - Side-by-side comparison

## Features Highlighted

The documentation showcases:
- **Tab alignment fixes** - Proper via connections between layers
- **Consistent via spacing** - Both circular and rectangular helix use same spacing
- **SVG visualizations** - Interactive previews of generated coils
- **Code examples** - Complete working examples for each coil type
- **Parameter explanations** - Detailed parameter descriptions and typical values

## Tips for Documentation

- Use descriptive SVG file names
- Include both "all layers" and "selective layers" views
- Provide complete code examples that users can copy-paste
- Explain the key improvements and fixes in the library
- Keep SVG file sizes reasonable for web viewing 