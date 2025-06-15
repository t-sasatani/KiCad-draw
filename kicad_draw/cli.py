"""Command-line interface for kicad-draw."""

import importlib.metadata
import sys

import click


def get_version() -> str:
    """Get the package version."""
    try:
        return importlib.metadata.version("kicad-draw")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


@click.group()
def main() -> None:
    """KiCad-draw CLI."""
    pass


@main.command()
def version() -> None:
    """Show the version and exit."""
    click.echo(f"kicad-draw version {get_version()}")
    sys.exit(0)


if __name__ == "__main__":
    main()
