"""Sphinx documentation configuration for KiCad-draw.

This module configures the Sphinx documentation builder
for generating API documentation and user guides.
"""

import os
import sys

html_theme = "furo"

sys.path.insert(0, os.path.abspath("../kicad_draw/"))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "KiCad-draw"
copyright = "2023, Takuya Sasatani"
author = "t-sasatani"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]

# MyST parser configuration
myst_enable_extensions = [
    "html_image",
    "substitution",
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Furo theme options -----------------------------------------------------
html_theme_options = {
    "source_repository": "https://github.com/t-sasatani/KiCad-draw/",
    "source_branch": "master",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#2980b9",
        "color-brand-content": "#2980b9",
    },
    "dark_css_variables": {
        "color-brand-primary": "#3498db",
        "color-brand-content": "#3498db",
    },
}

html_title = "KiCad-draw Documentation"

# GitHub Pages configuration
html_baseurl = "https://t-sasatani.github.io/KiCad-draw/"
