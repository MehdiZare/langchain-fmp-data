# Contributing to langchain-fmp-data

Thank you for your interest in contributing to langchain-fmp-data! We welcome contributions from the community and are grateful for any help you can provide.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Accept feedback gracefully

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check the [existing issues](https://github.com/MehdiZare/langchain-fmp-data/issues) to avoid duplicates
2. Create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Add relevant labels

### Submitting Pull Requests

1. **Fork the repository** and create your branch from `dev`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Set up your development environment**:
   ```bash
   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -

   # Install dependencies
   poetry install --with dev,test

   # Install pre-commit hooks
   poetry run pre-commit install
   ```

3. **Make your changes**:
   - Write clean, readable code
   - Follow existing code style and conventions
   - Add tests for new functionality
   - Update documentation as needed

4. **Run quality checks**:
   ```bash
   # Run tests
   poetry run pytest

   # Run linting and formatting
   poetry run ruff check langchain_fmp_data/
   poetry run ruff format langchain_fmp_data/

   # Run type checking
   poetry run mypy langchain_fmp_data/

   # Run all pre-commit hooks
   poetry run pre-commit run --all-files
   ```

5. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Follow conventional commits format:
     - `feat:` New features
     - `fix:` Bug fixes
     - `docs:` Documentation changes
     - `test:` Test additions or modifications
     - `refactor:` Code refactoring
     - `chore:` Maintenance tasks

6. **Push and create a Pull Request**:
   - Push to your fork
   - Create a PR against the `dev` branch
   - Fill out the PR template
   - Link related issues

### PR Labels

Add appropriate labels to your PR for automatic versioning:
- `major`: Breaking changes (1.0.0 → 2.0.0)
- `minor`: New features (1.0.0 → 1.1.0)
- `patch`: Bug fixes (1.0.0 → 1.0.1)
- `documentation`: Documentation updates
- `dependencies`: Dependency updates

## Development Guidelines

### Code Style

- We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- Line length: 100 characters
- Use type hints for all function parameters and returns
- Write docstrings for all public functions and classes

### Testing

- Write tests for all new functionality
- Maintain or improve code coverage (currently at 82%)
- Place unit tests in `tests/unit_tests/`
- Place integration tests in `tests/integration_tests/`
- Mock external API calls in unit tests

### Documentation

- Update README.md for user-facing changes
- Update CLAUDE.md for architectural changes
- Add docstrings to new functions and classes
- Include examples in docstrings when helpful

## Project Structure

```
langchain-fmp-data/
├── langchain_fmp_data/     # Main package code
│   ├── __init__.py         # Package exports
│   ├── agent.py            # LangGraph agent
│   ├── tools.py            # FMPDataTool
│   └── toolkits.py         # FMPDataToolkit
├── tests/                  # Test suite
│   ├── unit_tests/         # Unit tests
│   └── integration_tests/  # Integration tests
├── scripts/                # Utility scripts
├── .github/                # GitHub Actions
└── docs/                   # Additional documentation
```

## Release Process

1. PRs are merged to `dev` branch for testing
2. When ready for release, create PR from `dev` to `main`
3. Add appropriate version label (major/minor/patch)
4. Upon merge to `main`:
   - Version is automatically bumped
   - Package is published to PyPI
   - GitHub release is created

## Getting Help

- Check the [README](README.md) for basic usage
- Review [existing issues](https://github.com/MehdiZare/langchain-fmp-data/issues)
- Ask questions in [Discussions](https://github.com/MehdiZare/langchain-fmp-data/discussions)
- Contact maintainers for guidance

## Recognition

Contributors will be recognized in:
- The project's contributor list
- Release notes for significant contributions
- Special mentions for exceptional help

Thank you for contributing to langchain-fmp-data!
