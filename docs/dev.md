# Development Guide

## Testing

We use pytest for testing. The tests are located in the `tests` directory. To run the tests, use:

```sh
pytest
```

### Recent Fixes

- Updated the expected output in `tests/test_PCBdraw.py` to match the current output format (removed leading spaces) while maintaining strict test assertions.

## Code Quality

We use the following tools to maintain code quality:

- **Black**: For code formatting. Run with:
  ```sh
  black .
  ```

- **isort**: For import sorting. Run with:
  ```sh
  isort .
  ```

- **Ruff**: For linting. Run with:
  ```sh
  ruff check .
  ```

## Dependency Management

We use `uv` for dependency management. To install dependencies, run:

```sh
uv pip install -e .
```

## Building Documentation

To build the documentation using Sphinx, run:

```sh
cd docs
make html
```

The built documentation will be available in `docs/_build/html`.

## Using Poetry and uv for Development

### Poetry

Poetry is used for dependency management and packaging. To get started:

1. **Install Poetry**: Follow the [official installation guide](https://python-poetry.org/docs/#installation).
2. **Set Up Your Project**: Use `poetry init` to create a `pyproject.toml` file.
3. **Install Dependencies**: Run `poetry install` to install all dependencies.
4. **Add Dependencies**: Use `poetry add <package>` to add new packages.
5. **Build Your Project**: Use `poetry build` to build your project.

### uv

uv is a fast tool for managing Python virtual environments and dependencies. To use it:

1. **Install uv**: Follow the [official installation guide](https://github.com/uv-project/uv).
2. **Create a Virtual Environment**: Use `uv venv` to create a new virtual environment.
3. **Activate the Environment**: Activate the environment using the appropriate command for your shell (e.g., `source .venv/bin/activate` on Unix).
4. **Install Dependencies**: Use `uv pip install <package>` to install packages.

### Using Both Tools

You can use both Poetry and uv in your development workflow:

- **Poetry**: Use for managing project dependencies and building packages.
- **uv**: Use for quickly creating and managing virtual environments.

Ensure that both tools are configured to use the same Python version and dependencies to avoid conflicts. 