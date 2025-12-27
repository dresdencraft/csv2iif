# Contributing to csv2iif

## Commit Message Format

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for semantic versioning:

- `feat:` - New feature (minor version bump)
- `fix:` - Bug fix (patch version bump)
- `docs:` - Documentation changes
- `perf:` - Performance improvements (patch version bump)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `ci:` - CI/CD changes
- `chore:` - Other changes

Example:
```
feat: add support for multiple date formats
fix: handle empty CSV files correctly
docs: update installation instructions
```

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

1. Create a new branch from `master`
2. Use conventional commit messages (see above)
3. Make your changes
4. Run tests and linting locally
5. Push your branch and create a pull request
6. Ensure CI passes (tests + coverage ≥95%)
7. Wait for review and approval

## Code Standards

- Python 3.12+
- 95%+ test coverage required
- All lint checks must pass
- Follow existing code style
- Add tests for new features
- Use conventional commit messages

## Release Process

Releases are automated using semantic versioning:
- Merges to `master` trigger the release workflow
- Requires manual approval in GitHub Actions
- Version is determined by commit messages (feat/fix/etc.)
- Creates git tag and GitHub release automatically
