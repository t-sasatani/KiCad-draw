# Development Guide

## Testing

We use pytest for testing. The tests are located in the `tests` directory. To run the tests, use:

```sh
uv run pytest
```

### Recent Fixes

- Updated the expected output in `tests/test_PCBdraw.py` to match the current output format (removed leading spaces) while maintaining strict test assertions.

## Code Quality

We use the following tools to maintain code quality:

- **Black**: For code formatting. Run with:
  ```sh
  uv run black .
  ```

- **isort**: For import sorting. Run with:
  ```sh
  uv run isort .
  ```

- **Ruff**: For linting. Run with:
  ```sh
  uv run ruff check .
  ```

## Dependency Management

We use `uv` for dependency management. To sync dependencies, run:

```sh
uv sync
```

## Building Documentation

To build the documentation using Sphinx, run:

```sh
uv run sphinx-build -b html docs docs/_build/html
```

The built documentation will be available in `docs/_build/html`.

## Development with uv

We use `uv` for fast Python package and dependency management:

1. **Install uv**: Follow the [official installation guide](https://github.com/astral-sh/uv).
2. **Sync Dependencies**: Run `uv sync` to create/update the virtual environment with locked dependencies.
3. **Run Commands**: Use `uv run <command>` to run commands in the project environment.
4. **Add Dependencies**: Use `uv add <package>` to add new dependencies (automatically updates `uv.lock`). 