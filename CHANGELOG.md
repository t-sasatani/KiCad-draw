# Changelog

All notable changes to KiCad-draw will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] - 2025-06-15

### Fixed
- GitHub Actions publishing workflow now includes required `build` package
- Documentation deployment switched from Read the Docs to GitHub Pages
- Duplicate changelog entries removed from documentation sidebar

### Changed  
- Documentation now hosted on GitHub Pages for better integration
- Simplified README to minimize maintenance overhead
- Improved development workflow with proper build dependencies

### Infrastructure
- Added `build` package to dev dependencies for reliable package building
- Streamlined documentation build process with GitHub Actions
- Eliminated Read the Docs configuration complexity

## [0.4.1] - 2025-06-15

### Added
- Automated PyPI publishing workflow using GitHub Actions
- Trusted Publisher (OIDC) integration for secure, credential-free PyPI publishing
- Automated GitHub Releases creation with changelog information
- Multi-Python version testing (3.9-3.12) in CI pipeline

### Changed
- Modernized release process - publishing now triggered by git tag pushes
- Enhanced security by eliminating need for API token management
- Streamlined development workflow with automated testing and publishing

### Infrastructure
- Added comprehensive GitHub Actions workflow for automated releases
- Integrated with PyPI Trusted Publishers for secure publishing
- Automated package building and distribution process

## [0.4.0] - 2025-06-15

### Added
- Comprehensive Sphinx documentation with SVG visualizations
- Interactive examples with embedded SVG previews
- Quick start guide for new users
- Automated SVG generation script for documentation
- Via spacing consistency between circular and rectangular helix functions

### Fixed
- **CRITICAL**: Tab alignment issue in rectangular helix coils - tabs now properly connect between adjacent layers
- Via spacing inconsistency - both coil types now use same spacing algorithm (~0.65mm vs previous 3.0mm difference)
- Test suite updated to use new HelixParams API
- Code formatting and linting issues (18 fixes)

### Changed
- Rectangular helix port calculation now uses `port_gap` directly for consistent spacing
- Documentation structure reorganized with examples and quickstart sections
- All tests now pass with 100% success rate

### Technical Details
- Tab traces now align properly: bottom tab of layer N connects to top tab of layer N-1
- Via spacing reduced from 4.4x difference to only 0.033 units difference between coil types
- Added 5 comprehensive SVG examples showcasing both coil types

## [0.3.0] - 2024-XX-XX

### Added
- Rectangular helix coil support with `HelixRectangleParams`
- Rounded corner support for rectangular coils
- Port and tab connection system for rectangular coils
- Enhanced visualization with layer-specific colors

### Changed
- Improved PCBdraw API with parameter objects
- Better layer management and stackup support

## [0.2.1] - 2024-XX-XX

### Fixed
- Visualization rendering issues
- Layer ordering in SVG output
- Via positioning accuracy

### Changed
- Optimized SVG generation performance

## [0.2.0] - 2024-XX-XX

### Added
- SVG visualization support
- Multi-layer stackup support (4-layer and 6-layer)
- Interactive layer visibility controls
- Layer legend and color coding

### Changed
- Refactored visualization architecture
- Improved modular design

## [0.1.1] - 2024-XX-XX

### Fixed
- Installation and dependency issues
- API stability improvements
- Documentation corrections

### Added
- Basic examples and usage documentation

## [0.1.0] - 2024-XX-XX

### Added
- Initial release of KiCad-draw
- Circular helix coil generation with `HelixParams`
- KiCad s-expression output support
- Basic PCB layer management
- Via and trace generation
- Core drawing primitives (lines, arcs, vias)
- Support for multi-layer coil designs

### Features
- Generate PCB coil patterns compatible with KiCad
- Customizable coil parameters (radius, track width, layer count)
- Proper via connections between layers
- Export to KiCad-compatible format

---

## Version Comparison

| Version | Key Features | Breaking Changes |
|---------|-------------|------------------|
| 0.4.2 | GitHub Pages docs, build fixes, streamlined maintenance | None |
| 0.4.1 | Automated publishing, GitHub Actions, trusted publishers | None |
| 0.4.0 | Tab alignment fix, via spacing consistency, comprehensive docs | None |
| 0.3.0 | Rectangular coils, enhanced visualization | Parameter object API |
| 0.2.0 | SVG visualization, multi-layer support | Visualization API |
| 0.1.0 | Basic circular coils, KiCad export | Initial release |

## Migration Guide

### From 0.4.1 to 0.4.2
- No breaking changes - pure infrastructure improvements  
- No code changes required - same API
- Documentation now on GitHub Pages instead of Read the Docs
- Development builds now more reliable with proper dependencies

### From 0.4.0 to 0.4.1
- No breaking changes - pure infrastructure improvements
- No code changes required - same API
- Automated publishing now available for maintainers

### From 0.3.x to 0.4.0
- No breaking changes - all existing code continues to work
- Rectangular helix coils now have proper tab alignment automatically
- Consider using new documentation examples for best practices

### From 0.2.x to 0.3.0
- Update `draw_helix()` calls to use `HelixParams` objects instead of individual parameters
- Rectangular coils require `HelixRectangleParams` objects

## Contributors

- **t-sasatani** - Original author and maintainer
- **Claude (Anthropic)** - v0.4.0 improvements and documentation 