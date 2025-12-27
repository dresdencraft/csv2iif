# Contributing to csv2iif

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/dresdencraft/csv2iif.git
cd csv2iif
```

2. Install development dependencies:
```bash
make install-dev
```

3. Install the package in editable mode:
```bash
pip install -e .
```

## Running Tests

```bash
make test
```

## Linting

```bash
make lint
```

## Formatting

```bash
make format
```

## Pull Request Process

1. Create a new branch from `main`
2. Make your changes
3. Run tests and linting locally
4. Push your branch and create a pull request
5. Ensure CI passes
6. Wait for review and approval

## Code Standards

- Python 3.12+
- 98%+ test coverage required
- All lint checks must pass
- Follow existing code style
- Add tests for new features
