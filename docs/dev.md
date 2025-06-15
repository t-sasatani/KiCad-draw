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